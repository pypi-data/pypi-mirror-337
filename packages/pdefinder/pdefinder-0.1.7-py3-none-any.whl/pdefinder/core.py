"""
Module: core.py
This module contains helper functions for PDE-FIND as well as a main pipeline function
that runs the discovery process.
"""

import numpy as np
import scipy.io as sio
import re
import json
import torch
from openai import OpenAI
# from np import real
import scipy
import itertools
import operator
import scipy.sparse as sparse
from scipy.sparse import csc_matrix, dia_matrix

# ------------------------------
# Helper functions for PDE-FIND
# ------------------------------

def STRidge(X0, y, lam, maxit, tol, normalize, print_results=False):
    if normalize:
        nX0 = np.linalg.norm(X0, axis=0)
        X0_norm = X0 / (nX0 + 1e-10)
    else:
        X0_norm = X0

    w = np.linalg.lstsq(X0_norm, y, rcond=None)[0]

    for it in range(maxit):
        biginds = np.where(np.abs(w) > tol)[0]
        if len(biginds) == 0:
            w = np.zeros_like(w)
            break
        w_new = np.linalg.lstsq(X0_norm[:, biginds], y, rcond=None)[0]
        w_temp = np.zeros_like(w)
        w_temp[biginds] = w_new.reshape(-1,1)
        w = w_temp
    if normalize:
        w = w / (nX0.reshape(-1,1) + 1e-10)
    return w

def TrainSTRidge(R, Ut, lam, d_tol, maxit=25, STR_iters=10, l0_penalty=None, normalize=2, split=0.8, print_best_tol=False):
    np.random.seed(0)  # for consistency
    n, _ = R.shape
    train = np.random.choice(n, int(n*split), replace=False)
    test = [i for i in np.arange(n) if i not in train]
    TrainR = R[train, :]
    TestR = R[test, :]
    TrainY = Ut[train, :]
    TestY = Ut[test, :]
    D = TrainR.shape[1]

    d_tol = float(d_tol)
    tol = d_tol
    if l0_penalty is None:
        l0_penalty = 0.001 * np.linalg.cond(R)

    w = np.zeros((D, 1))
    w_best = np.linalg.lstsq(TrainR, TrainY, rcond=None)[0]
    err_best = np.linalg.norm(TestY - TestR.dot(w_best), 2) + l0_penalty * np.count_nonzero(w_best)
    tol_best = 0

    for iter in range(maxit):
        w = STRidge(TrainR, TrainY, lam, STR_iters, tol, normalize=normalize)
        err = np.linalg.norm(TestY - TestR.dot(w), 2) + l0_penalty * np.count_nonzero(w)

        if err <= err_best:
            err_best = err
            w_best = w
            tol_best = tol
            tol = tol + d_tol
        else:
            tol = max([0, tol - 2 * d_tol])
            d_tol = 2 * d_tol / (maxit - iter)
            tol = tol + d_tol

    if print_best_tol:
        print("Optimal tolerance:", tol_best)
    return w_best

def TikhonovDiff(f, dx, lam, d = 1):
    n = len(f)
    f = np.matrix(f - f[0]).reshape((n,1))
    A = np.zeros((n,n))
    for i in range(1, n):
        A[i,i] = dx/2
        A[i,0] = dx/2
        for j in range(1,i):
            A[i,j] = dx
    e = np.ones(n-1)
    D = sparse.diags([e, -e], [1, 0], shape=(n-1, n)).todense() / dx
    g = np.squeeze(np.asarray(np.linalg.lstsq(A.T.dot(A) + lam*D.T.dot(D), A.T.dot(f), rcond=None)[0]))
    if d == 1: 
        return g
    else:
        return FiniteDiff(g, dx, d-1)

def FiniteDiff(u, dx, d):
    n = u.size
    ux = np.zeros(n, dtype=np.complex64)
    if d == 1:
        for i in range(1,n-1):
            ux[i] = (u[i+1]-u[i-1]) / (2*dx)
        ux[0] = (-3.0/2*u[0] + 2*u[1] - u[2]/2) / dx
        ux[n-1] = (3.0/2*u[n-1] - 2*u[n-2] + u[n-3]/2) / dx
        return ux
    if d == 2:
        for i in range(1,n-1):
            ux[i] = (u[i+1]-2*u[i]+u[i-1]) / dx**2
        ux[0] = (2*u[0] - 5*u[1] + 4*u[2] - u[3]) / dx**2
        ux[n-1] = (2*u[n-1] - 5*u[n-2] + 4*u[n-3] - u[n-4]) / dx**2
        return ux
    if d == 3:
        for i in range(2,n-2):
            ux[i] = (u[i+2]/2 - u[i+1] + u[i-1] - u[i-2]/2) / dx**3
        ux[0] = (-2.5*u[0]+9*u[1]-12*u[2]+7*u[3]-1.5*u[4]) / dx**3
        ux[1] = (-2.5*u[1]+9*u[2]-12*u[3]+7*u[4]-1.5*u[5]) / dx**3
        ux[n-1] = (2.5*u[n-1]-9*u[n-2]+12*u[n-3]-7*u[n-4]+1.5*u[n-5]) / dx**3
        ux[n-2] = (2.5*u[n-2]-9*u[n-3]+12*u[n-4]-7*u[n-5]+1.5*u[n-6]) / dx**3
        return ux
    if d > 3:
        return FiniteDiff(FiniteDiff(u,dx,3), dx, d-3)

def ConvSmoother(x, p, sigma):
    n = len(x)
    y = np.zeros(n, dtype=np.complex64)
    g = np.exp(-np.power(np.linspace(-p, p, 2*p),2) / (2.0*sigma**2))
    for i in range(n):
        a = max([i-p,0])
        b = min([i+p,n])
        c = max([0, p-i])
        d = min([2*p, p+n-i])
        y[i] = np.sum(np.multiply(x[a:b], g[c:d]))/np.sum(g[c:d])
    return y

def PolyDiff(u, x, deg=3, diff=1, width=5):
    u = u.flatten()
    x = x.flatten()
    n = len(x)
    du = np.zeros((n - 2*width, diff))
    for j in range(width, n-width):
        points = np.arange(j - width, j + width + 1)
        poly = np.polynomial.chebyshev.Chebyshev.fit(x[points], u[points], deg)
        for d in range(1, diff+1):
            du[j-width, d-1] = poly.deriv(m=d)(x[j])
    return du

def PolyDiffPoint(u, x, deg=3, diff=1, index=None):
    n = len(x)
    if index is None: 
        index = (n-1)//2
    poly = np.polynomial.chebyshev.Chebyshev.fit(x, u, deg)
    derivatives = []
    for d in range(1, diff+1):
        derivatives.append(poly.deriv(m=d)(x[index]))
    return derivatives

def build_Theta(data, derivatives, derivatives_description, P, data_description=None):
    n, d = data.shape
    m, d2 = derivatives.shape
    if n != m: 
        raise Exception('dimension error')
    if data_description is not None: 
        if len(data_description) != d:
            raise Exception('data description error')
    rhs_functions = {}
    f = lambda x, y: np.prod(np.power(list(x), list(y)))
    powers = []            
    for p in range(1, P+1):
        size = d + p - 1
        for indices in itertools.combinations(range(size), d-1):
            starts = [0] + [index+1 for index in indices]
            stops = indices + (size,)
            powers.append(tuple(map(operator.sub, stops, starts)))
    for power in powers:
        rhs_functions[power] = [lambda x, y=power: f(x,y), power]
    Theta = np.ones((n,1), dtype=np.complex64)
    descr = ['']
    for D in range(1, derivatives.shape[1]):
        Theta = np.hstack([Theta, derivatives[:,D].reshape(n,1)])
        descr.append(derivatives_description[D])
    for D in range(derivatives.shape[1]):
        for k in rhs_functions.keys():
            func = rhs_functions[k][0]
            new_column = np.zeros((n,1), dtype=np.complex64)
            for i in range(n):
                new_column[i] = func(data[i,:]) * derivatives[i, D]
            Theta = np.hstack([Theta, new_column])
            if data_description is None:
                descr.append(str(rhs_functions[k][1]) + derivatives_description[D])
            else:
                function_description = ''
                for j in range(d):
                    if rhs_functions[k][1][j] != 0:
                        if rhs_functions[k][1][j] == 1:
                            function_description += data_description[j]
                        else:
                            function_description += data_description[j] + '^' + str(rhs_functions[k][1][j])
                descr.append(function_description + derivatives_description[D])
    return Theta, descr

def build_linear_system(u, dt, dx, D=3, P=3, time_diff='poly', space_diff='poly', lam_t=None, lam_x=None, width_x=None, width_t=None, deg_x=5, deg_t=None, sigma=2):
    n, m = u.shape
    if width_x is None: 
        width_x = n//10
    if width_t is None: 
        width_t = m//10
    if deg_t is None: 
        deg_t = deg_x
    if time_diff == 'poly': 
        m2 = m - 2*width_t
        offset_t = width_t
    else: 
        m2 = m
        offset_t = 0
    if space_diff == 'poly': 
        n2 = n - 2*width_x
        offset_x = width_x
    else: 
        n2 = n
        offset_x = 0
    if lam_t is None: 
        lam_t = 1.0/m
    if lam_x is None: 
        lam_x = 1.0/n

    ut = np.zeros((n2, m2), dtype=np.complex64)
    if time_diff == 'FDconv':
        Usmooth = np.zeros((n, m), dtype=np.complex64)
        for j in range(m):
            Usmooth[:,j] = ConvSmoother(u[:,j], width_t, sigma)
        for i in range(n2):
            ut[i,:] = FiniteDiff(Usmooth[i + offset_x,:], dt, 1)
    elif time_diff == 'poly':
        T = np.linspace(0, (m-1)*dt, m)
        for i in range(n2):
            ut[i,:] = PolyDiff(u[i+offset_x,:], T, diff=1, width=width_t, deg=deg_t)[:,0]
    elif time_diff == 'Tik':
        for i in range(n2):
            ut[i,:] = TikhonovDiff(u[i + offset_x,:], dt, lam_t)
    else:
        for i in range(n2):
            ut[i,:] = FiniteDiff(u[i + offset_x,:], dt, 1)
    ut = np.reshape(ut, (n2*m2, 1), order='F')

    u2 = u[offset_x:n-offset_x, offset_t:m-offset_t]
    Theta = np.zeros((n2*m2, (D+1)*(P+1)), dtype=np.complex64)
    ux = np.zeros((n2, m2), dtype=np.complex64)
    rhs_description = ['' for i in range((D+1)*(P+1))]

    if space_diff == 'poly': 
        Du = {}
        for i in range(m2):
            Du[i] = PolyDiff(u[:,i+offset_t], np.linspace(0, (n-1)*dx, n), diff=D, width=width_x, deg=deg_x)
    if space_diff == 'Fourier':
        ik = 1j * np.fft.fftfreq(n) * n

    for d in range(D+1):
        if d > 0:
            for i in range(m2):
                if space_diff == 'Tik': 
                    ux[:,i] = TikhonovDiff(u[:,i+offset_t], dx, lam_x, d=d)
                elif space_diff == 'FDconv':
                    Usmooth = ConvSmoother(u[:,i+offset_t], width_x, sigma)
                    ux[:,i] = FiniteDiff(Usmooth, dx, d)
                elif space_diff == 'FD': 
                    ux[:,i] = FiniteDiff(u[:,i+offset_t], dx, d)
                elif space_diff == 'poly': 
                    ux[:,i] = Du[i][:,d-1]
                elif space_diff == 'Fourier': 
                    ux[:,i] = np.fft.ifft(ik**d * np.fft.fft(ux[:,i]))
        else:
            ux = np.ones((n2, m2), dtype=np.complex64)
            
        for p in range(P+1):
            Theta[:, d*(P+1)+p] = np.reshape(np.multiply(ux, np.power(u2, p)), (n2*m2), order='F')
            if p == 1:
                rhs_description[d*(P+1)+p] = 'u'
            elif p > 1:
                rhs_description[d*(P+1)+p] = 'u^' + str(p)
            if d > 0:
                rhs_description[d*(P+1)+p] += 'u_' + ''.join(['x' for _ in range(d)])
    return ut, Theta, rhs_description

def print_pde(w, rhs_description, ut='u_t'):
    pde = ut + ' = '
    first = True
    for i in range(len(w)):
        if w[i] != 0:
            if not first:
                pde += ' + '
            pde += "(%05f %+05fi)" % (w[i].real, w[i].imag) + rhs_description[i] + "\n   "
            first = False
    print(pde)

def Lasso(X0, Y, lam, w=np.array([0]), maxit=100, normalize=2):
    n, d = X0.shape
    X = np.zeros((n, d), dtype=np.complex64)
    Y = Y.reshape(n,1)
    if w.size != d:
        w = np.zeros((d,1), dtype=np.complex64)
    w_old = np.zeros((d,1), dtype=np.complex64)
    if normalize != 0:
        Mreg = np.zeros((d,1))
        for i in range(d):
            Mreg[i] = 1.0/(np.linalg.norm(X0[:,i], normalize))
            X[:,i] = Mreg[i]*X0[:,i]
    else:
        X = X0
    L = np.linalg.norm(X.T.dot(X), 2)
    for iters in range(maxit):
        z = w + iters/float(iters+1)*(w - w_old)
        w_old = w
        z = z - X.T.dot(X.dot(z)-Y)/L
        for j in range(d):
            w[j] = np.multiply(np.sign(z[j]), np.max([abs(z[j])-lam/L,0]))
    biginds = np.where(w != 0)[0]
    if biginds != []:
        w[biginds] = np.linalg.lstsq(X[:, biginds], Y, rcond=None)[0]
    if normalize != 0:
        return np.multiply(Mreg, w)
    else:
        return w

def ElasticNet(X0, Y, lam1, lam2, w=np.array([0]), maxit=100, normalize=2):
    n, d = X0.shape
    X = np.zeros((n, d), dtype=np.complex64)
    Y = Y.reshape(n,1)
    if w.size != d:
        w = np.zeros((d,1), dtype=np.complex64)
    w_old = np.zeros((d,1), dtype=np.complex64)
    if normalize != 0:
        Mreg = np.zeros((d,1))
        for i in range(d):
            Mreg[i] = 1.0/(np.linalg.norm(X0[:,i], normalize))
            X[:,i] = Mreg[i]*X0[:,i]
    else:
        X = X0
    L = np.linalg.norm(X.T.dot(X), 2) + lam2
    for iters in range(maxit):
        z = w + iters/float(iters+1)*(w - w_old)
        w_old = w
        z = z - (lam2*z + X.T.dot(X.dot(z)-Y))/L
        for j in range(d):
            w[j] = np.multiply(np.sign(z[j]), np.max([abs(z[j])-lam1/L,0]))
    biginds = np.where(w != 0)[0]
    if biginds != []:
        w[biginds] = np.linalg.lstsq(X[:, biginds], Y, rcond=None)[0]
    if normalize != 0:
        return np.multiply(Mreg, w)
    else:
        return w

def FoBaGreedy(X, y, epsilon=0.1, maxit_f=100, maxit_b=5, backwards_freq=5, relearn_f=True, relearn_b=True):
    n, d = X.shape
    F = {}
    F[0] = set()
    w = {}
    w[0] = np.zeros((d,1))
    k = 0
    delta = {}

    for forward_iter in range(maxit_f):
        k = k+1
        zero_coeffs = np.where(w[k-1] == 0)[0]
        if len(zero_coeffs)==0:
            return w[k-1]
        err_after_addition = []
        residual = y - X.dot(w[k-1])
        for i in zero_coeffs:
            if relearn_f:
                F_trial = F[k-1].union({i})
                w_added = np.zeros((d,1))
                w_added[list(F_trial)] = np.linalg.lstsq(X[:, list(F_trial)], y, rcond=None)[0]
            else:
                alpha = X[:,i].T.dot(residual)/np.linalg.norm(X[:,i])**2
                w_added = np.copy(w[k-1])
                w_added[i] = alpha
            err_after_addition.append(np.linalg.norm(X.dot(w_added)-y))
        i = zero_coeffs[np.argmin(err_after_addition)]
        F[k] = F[k-1].union({i})
        w[k] = np.zeros((d,1), dtype=np.complex64)
        w[k][list(F[k])] = np.linalg.lstsq(X[:, list(F[k])], y, rcond=None)[0]
        delta[k] = np.linalg.norm(X.dot(w[k-1]) - y) - np.linalg.norm(X.dot(w[k]) - y)
        if delta[k] < epsilon:
            return w[k-1]
        if forward_iter % backwards_freq == 0 and forward_iter > 0:
            for backward_iter in range(maxit_b):
                non_zeros = np.where(w[k] != 0)[0]
                err_after_simplification = []
                for j in non_zeros:
                    if relearn_b:
                        F_trial = F[k].difference({j})
                        w_simple = np.zeros((d,1))
                        w_simple[list(F_trial)] = np.linalg.lstsq(X[:, list(F_trial)], y, rcond=None)[0]
                    else:
                        w_simple = np.copy(w[k])
                        w_simple[j] = 0
                    err_after_simplification.append(np.linalg.norm(X.dot(w_simple) - y))
                j = np.argmin(err_after_simplification)
                w_simple = np.copy(w[k])
                w_simple[non_zeros[j]] = 0
                delta_p = err_after_simplification[j] - np.linalg.norm(X.dot(w[k]) - y)
                if delta_p > 0.5*delta[k]:
                    break
                k = k-1
                F[k] = F[k+1].difference({j})
                w[k] = np.zeros((d,1))
                w[k][list(F[k])] = np.linalg.lstsq(X[:, list(F[k])], y, rcond=None)[0]
    return w[k]

def subsample_data(u, x, t, spatial_factor=8, temporal_factor=8):
    u_sub = u[::temporal_factor, ::spatial_factor]
    x_sub = x[::spatial_factor]
    t_sub = t[::temporal_factor]
    return u_sub, x_sub, t_sub

def print_and_save_pde(w, rhs_description, ut='u_t', file_path='discovered_pde.txt'):
    threshold = 0.1
    pde = ut + ' = '
    first = True
    for i in range(len(w)):
        val = w[i].item() if hasattr(w[i], 'item') else w[i]
        if abs(val.real) < threshold:
            continue
        if not first:
            pde += ' + '
        if abs(val.imag) < 1e-8:
            pde += "{:+.2f}".format(val.real) + rhs_description[i]
        else:
            pde += "({:+.2f} {:+.2f}i)".format(val.real, val.imag) + rhs_description[i]
        first = False
    print(pde)
    with open(file_path, 'w') as f:
        f.write(pde)
    return pde

def print_and_save_pde_func_final(w, rhs_description, candidate_terms, ver_coeffs, ut='u_t', file_path='discovered_pde.txt'):
    pde = ut + ' = '
    first = True
    for j, term in enumerate(candidate_terms):
        if term not in rhs_description:
            continue
        i = rhs_description.index(term)
        val = w[i].item() if hasattr(w[i], 'item') else w[i]
        if ver_coeffs[j] != 0 and np.sign(val.real) != np.sign(ver_coeffs[j]):
            val = -val
        if not first:
            pde += ' + '
        if abs(val.imag) < 1e-8:
            pde += "{:+.2f}".format(val.real) + term
        else:
            pde += "({:+.2f} {:+.2f}i)".format(val.real, val.imag) + term
        first = False
    print(pde)
    with open(file_path, 'w') as f:
        f.write(pde)
    return pde

# def extract_terms_from_pde(pde_str):
#     terms = re.findall(r'[-+]?\d*\.\d+\s*([a-zA-Z0-9_{}\^]+)', pde_str)
#     return terms

def extract_terms_from_pde(pde_str):
    # This regex matches either:
    #   - a parenthesized coefficient (e.g., "(0.000009 +0.500330i)")
    #   - or a plain float (e.g., "+1.23")
    # and then captures the candidate term that follows.
    terms = re.findall(r'(?:\([^)]+\)|[-+]?\d*\.\d+)\s*([a-zA-Z0-9_{}\^\|]+)', pde_str)
    return terms

def load_ns_data(data_dir="."):


    data = scipy.io.loadmat(f"{data_dir}/Vorticity_ALL.mat")        
    steps = 151
    n = 449
    m = 199
    dt = 0.2
    dx = 0.02
    dy = 0.02
    
    xmin = 100
    xmax = 425
    ymin = 15
    ymax = 185 
    W = data['VORTALL'].reshape(n,m,steps)   # vorticity
    U = data['UALL'].reshape(n,m,steps)      # x-component of velocity
    V = data['VALL'].reshape(n,m,steps)      # y-component of velocity  
    W = W[xmin:xmax,ymin:ymax,:]
    U = U[xmin:xmax,ymin:ymax,:]
    V = V[xmin:xmax,ymin:ymax,:]
    n,m,steps = W.shape

    np.random.seed(0)

    num_xy = 2000
    num_t = 50
    num_points = num_xy * num_t
    boundary = 5
    boundary_x = 10
    points = {}
    count = 0

    for p in range(num_xy):
        x = np.random.choice(np.arange(boundary_x,n-boundary_x),1)[0]
        y = np.random.choice(np.arange(boundary,m-boundary),1)[0]
        for t in range(num_t):
            points[count] = [x,y,2*t+12]
            count = count + 1

    # Take up to second order derivatives.
    w = np.zeros((num_points,1))
    u = np.zeros((num_points,1))
    v = np.zeros((num_points,1))
    wt = np.zeros((num_points,1))
    wx = np.zeros((num_points,1))
    wy = np.zeros((num_points,1))
    wxx = np.zeros((num_points,1))
    wxy = np.zeros((num_points,1))
    wyy = np.zeros((num_points,1))

    N = 2*boundary-1  # odd number of points to use in fitting
    Nx = 2*boundary_x-1  # odd number of points to use in fitting
    deg = 5 # degree of polynomial to use
    # 
    i = 0
    for p in points.keys():
        i+=1
        [x,y,t] = points[p]
        w[p] = W[x,y,t]
        u[p] = U[x,y,t]
        v[p] = V[x,y,t]
        
        wt[p] = PolyDiffPoint(W[x,y,t-(N-1)//2:t+(N+1)//2], np.arange(N)*dt, deg, 1)[0]
        
        x_diff = PolyDiffPoint(W[x-(Nx-1)//2:x+(Nx+1)//2,y,t], np.arange(Nx)*dx, deg, 2)
        y_diff = PolyDiffPoint(W[x,y-(N-1)//2:y+(N+1)//2,t], np.arange(N)*dy, deg, 2)
        wx[p] = x_diff[0]
        wy[p] = y_diff[0]
        
        x_diff_yp = PolyDiffPoint(W[x-(Nx-1)//2:x+(Nx+1)//2,y+1,t], np.arange(Nx)*dx, deg, 2)
        x_diff_ym = PolyDiffPoint(W[x-(Nx-1)//2:x+(Nx+1)//2,y-1,t], np.arange(Nx)*dx, deg, 2)
        
        wxx[p] = x_diff[1]
        wxy[p] = (x_diff_yp[0]-x_diff_ym[0])/(2*dy)
        wyy[p] = y_diff[1]
    return w,u,v,wt, wx,wxx,wy, wyy, wxy

def data_load(dataset, data_dir="."):
    """
    Loads the specified dataset from a given directory.
    
    Parameters:
      dataset : str, name of the dataset ('chafee-infante', 'Burgers', 'KS', etc.)
      data_dir: str, path to the directory where the dataset files are stored.
    
    Returns:
      u, x, t : Data arrays loaded from the dataset.
    """
    if dataset == 'chafee-infante':
        u = np.load(f"{data_dir}/chafee_infante_CI.npy")
        x = np.load(f"{data_dir}/chafee_infante_x.npy").reshape(-1,1)
        t = np.load(f"{data_dir}/chafee_infante_t.npy").reshape(-1,1)
    elif dataset == 'Burgers':
        data = sio.loadmat(f"{data_dir}/burgers.mat")
        u = data.get("usol")
        x = np.squeeze(data.get("x")).reshape(-1,1)
        t = np.squeeze(data.get("t")).reshape(-1,1)
    elif dataset == 'KS':
        data = sio.loadmat(f"{data_dir}/kuramoto_sivishinky.mat")
        u = data['uu']
        x = data['x'][:,0].reshape(-1,1)
        t = data['tt'][0,:].reshape(-1,1)
    elif dataset == 'kdv':
        data = sio.loadmat(f"{data_dir}/kdv.mat")
        u = np.real(data['usol'])
        x = data['x'][0]
        t = data['t'][:,0]

    elif dataset == "fisher":
    
        data=scipy.io.loadmat(f"{data_dir}/fisher_nonlin_groundtruth.mat")

        # D=data['D'] #0.02
        # r=data['r'] #10
        # K=data['K']
        x=np.squeeze(data['x'])[1:-1].reshape(-1,1)[3:-3]
        t=np.squeeze(data['t'])[1:-1].reshape(-1,1)[3:-3]
        u=data['U'][3:-3,3:-3][1:-1,1:-1].T

    # elif dataset == 'NS':
    #     w,u,v,w_t, w_x, w_xx, w_y, w_yy, w_xy = load_ns_data()
    #     # feature_dict['x'] = x_data.reshape(-1)
    #     w_x = w_x.reshape(-1)
    #     w_xx= w_xx.reshape(-1)
    #     w_y = w_y.reshape(-1)
    #     w_yy = w_yy.reshape(-1)
    #     w = w.reshape(-1)
    #     u = u.reshape(-1)
    #     v = v.reshape(-1)
    #     w_xy = w_xy.reshape(-1)
    #     return w_t.reshape(-1,1), w,u,v,w_x, w_xx, w_y, w_yy, w_xy

    else:
        raise Exception("Unknown dataset")
    return u, x, t

def subsample_candidate_matrix(R, Ut, new_num_rows):
    total_rows = R.shape[0]
    if new_num_rows >= total_rows:
        return R, Ut
    idx = np.random.choice(total_rows, new_num_rows, replace=False)
    return R[idx, :], Ut[idx, :]

def llm_get_coefficients(terms,llm_name):
    prompt = (f"Your task is to return a JSON array of exactly {len(terms)} numeric coefficients corresponding to "
              f"the PDE terms {terms}. Do not include any additional text.")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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"  # Replace with your API key.
    )
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",
            "X-Title": "<YOUR_SITE_NAME>",
        },
        extra_body={},
        model=llm_name,
        messages=[{"role": "user", "content": prompt}]
    )
    response = completion.choices[0].message.content
    print("LLM response:", response)
    try:
        coeffs = json.loads(response)
        if isinstance(coeffs, list) and len(coeffs) == len(terms):
            return np.array(coeffs, dtype=float)
    except Exception:
        pass
    coeffs_list = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', response)
    if len(coeffs_list) < len(terms):
        print("Warning: Not enough coefficients extracted; defaulting missing values to 1.0.")
        coeffs = [float(c) for c in coeffs_list] + [1.0]*(len(terms) - len(coeffs_list))
        return np.array(coeffs)
    coeffs = [float(c) for c in coeffs_list[:len(terms)]]
    return np.array(coeffs)

def verify_llm(candidate_terms, llm_name):
    client_verify = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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"  # Replace with your API key.
    )
    prompt = (
        f"You are a PDE expert. Based solely on the candidate PDE terms {candidate_terms}, "
        "infer which PDE this structure most closely represents. Then, using your expert knowledge, "
        "return a JSON object with exactly two keys: 'pde_name' and 'coefficients'. 'pde_name' should be a string "
        "representing your guessed PDE name, and 'coefficients' should be a JSON array of exactly " + 
        str(len(candidate_terms)) + " numeric coefficients that reflect the expected sign pattern and approximate "
        "magnitude for that PDE. Do not include any additional text or commentary in your response."
    )
    try:
        completion = client_verify.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",
                "X-Title": "<YOUR_SITE_NAME>",
            },
            extra_body={},
            model=llm_name,
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        print("Error calling verification LLM:", e)
        return "Unknown", np.ones(len(candidate_terms))
    
    if not completion or not completion.choices or len(completion.choices) == 0:
        print("No valid response from verification LLM; using default coefficients.")
        return "Unknown", np.ones(len(candidate_terms))
    
    try:
        response = completion.choices[0].message.content
    except Exception as e:
        print("Error accessing response content:", e)
        return "Unknown", np.ones(len(candidate_terms))
    
    print("Verification LLM response:", response)
    try:
        response_json = json.loads(response)
        pde_name = response_json.get("pde_name", "Unknown")
        coeffs = response_json.get("coefficients", [])
        if isinstance(coeffs, list) and len(coeffs) == len(candidate_terms):
            return pde_name, np.array(coeffs, dtype=float)
    except Exception as e:
        print("Error parsing JSON:", e)
    
    coeffs_list = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', response)
    if len(coeffs_list) < len(candidate_terms):
        print("Warning: Not enough coefficients extracted in verification; defaulting missing values to 1.0.")
        coeffs = [float(c) for c in coeffs_list] + [1.0]*(len(candidate_terms)-len(coeffs_list))
        return "Unknown", np.array(coeffs)
    coeffs = [float(c) for c in coeffs_list[:len(candidate_terms)]]
    return "Unknown", np.array(coeffs)



def run_nls_finder(u, dt, dx):
    """
    Runs the PDE discovery pipeline for NLS-type equations using build_Theta.
    
    Parameters:
      u  : 2D numpy array of the PDE solution (assumed shape: (m, n))
      dt : temporal grid spacing
      dx : spatial grid spacing
      
    Returns:
      w       : optimized coefficient vector (numpy array)
      pde_str : string representation of the discovered PDE
    """
    # Determine dimensions (assumed: m rows, n columns)
    m, n = u.shape

    # Compute time and spatial derivatives using finite differences.
    ut = np.zeros((m, n), dtype=np.complex64)
    ux = np.zeros((m, n), dtype=np.complex64)
    uxx = np.zeros((m, n), dtype=np.complex64)
    uxxx = np.zeros((m, n), dtype=np.complex64)

    for i in range(n):
        ut[:, i] = FiniteDiff(u[:, i], dt, 1)
    for i in range(m):
        ux[i, :]   = FiniteDiff(u[i, :], dx, 1)
        uxx[i, :]  = FiniteDiff(u[i, :], dx, 2)
        uxxx[i, :] = FiniteDiff(u[i, :], dx, 3)

    # Reshape the derivative arrays into column vectors (Fortran-order)
    ut    = np.reshape(ut,    (m * n, 1), order='F')
    ux    = np.reshape(ux,    (m * n, 1), order='F')
    uxx   = np.reshape(uxx,   (m * n, 1), order='F')
    uxxx  = np.reshape(uxxx,  (m * n, 1), order='F')

    # Construct the derivative matrix: constant, first, second, and third derivatives.
    X_ders = np.hstack([np.ones((m * n, 1)), ux, uxx, uxxx])

    # Construct the data matrix from the solution and its absolute value.
    X_data = np.hstack([np.reshape(u, (m * n, 1), order='F'),
                        np.reshape(np.abs(u), (m * n, 1), order='F')])
    # Descriptions for each derivative column.
    derivatives_description = ['', 'u_{x}', 'u_{xx}', 'u_{xxx}']

    # Build the candidate library using build_Theta (here using a polynomial up to degree 3).
    X, rhs_des = build_Theta(X_data, X_ders, derivatives_description, 3,
                             data_description=['u', '|u|'])

    # Run sparse regression using STRidge to get the coefficient vector.
    w = TrainSTRidge(X, ut, 10**-5, 500)
    
    # Print and return the discovered PDE.
    # print("PDE derived using STRidge for NLS-type equations")
    pde_str = print_pde(w, rhs_des)
    return w, pde_str

def print_pde(w, rhs_description, ut = 'u_t'):
    pde = ut + ' = '
    first = True
    for i in range(len(w)):
        if w[i] != 0:
            if not first:
                pde = pde + ' + '
            pde = pde + "(%05f %+05fi)" % (w[i].real, w[i].imag) + rhs_description[i] + "\n   "
            first = False
    print(pde)
    return pde


def run_ns_finder(data_dir="."):
    """
    Runs the Navier-Stokes PDE discovery pipeline using the NS data loader.
    
    The NS data loader (via data_load('NS', data_dir)) is expected to return:
      wt  : time derivative of vorticity w (as a column vector)
      w   : vorticity (as a 1D array, reshaped to column)
      u   : x-component of velocity
      v   : y-component of velocity
      wx, wxx, wy, wyy, wxy : corresponding spatial derivatives (all as 1D arrays)
    
    Returns:
      A tuple (c, description) where 'c' is the optimized coefficient vector
      and 'description' is the list of candidate term descriptions.
    """
    import numpy as np

    # Load NS data using the edited data loader for dataset 'NS'
    wt, w, u, v, wx, wxx, wy, wyy, wxy = data_load('NS', data_dir=data_dir)
    
    # Ensure that all outputs are reshaped to column vectors
    wt = wt.reshape(-1, 1)
    w = w.reshape(-1, 1)
    u = u.reshape(-1, 1)
    v = v.reshape(-1, 1)
    wx = wx.reshape(-1, 1)
    wxx = wxx.reshape(-1, 1)
    wy = wy.reshape(-1, 1)
    wyy = wyy.reshape(-1, 1)
    wxy = wxy.reshape(-1, 1)
    
    num_points = w.shape[0]
    
    # Build the candidate library using build_Theta.
    # X_data is built from [w, u, v].
    # X_ders is built from a column of ones and the spatial derivatives.
    X_data = np.hstack([w, u, v])
    X_ders = np.hstack([np.ones((num_points, 1)), wx, wy, wxx, wxy, wyy])
    X_ders_descr = ['', 'w_{x}', 'w_{y}', 'w_{xx}', 'w_{xy}', 'w_{yy}']
    
    # data_description corresponds to the columns in X_data.
    X, description = build_Theta(X_data, X_ders, X_ders_descr, 2, data_description=['w', 'u', 'v'])
    
    print("Candidate terms for PDE:")
    print(['1'] + description[1:])
    
    # Set STRidge parameters.
    lam = 10**-5
    d_tol = 5
    c = TrainSTRidge(X, wt, lam, d_tol)
    
    print("Derived PDE:")
    print_pde(c, description, ut='w_t')
    
    return c, description


# ------------------------------
# Main pipeline function
# ------------------------------

def run_pde_finder(dataset='KS', P=5, D=5, num_epochs=1000, data_dir=".",
                   llm_initial='default_llm', llm_verification='default_llm'):
    """
    Runs the PDE discovery pipeline.
    
    Parameters:
      dataset         : string, dataset name 
      P               : int, maximum polynomial power for candidate library (default pipeline)
      D               : int, maximum derivative order for candidate library (default pipeline)
      num_epochs      : int, number of epochs for PyTorch optimization (default pipeline)
      data_dir        : str, directory path where dataset files are located
      llm_initial     : str, identifier for the LLM used to generate initial coefficient guesses
      llm_verification: str, identifier for the LLM used for verification
       
    Returns:
      A tuple (w, pde_str) containing the optimized coefficient vector and PDE string.
    """
    print("Loading data...")
    # Case 1: Navier–Stokes dataset: trigger the NS pipeline.
    if dataset.lower() == 'ns':
        # print("Using Navier–Stokes pipeline...")
        return run_ns_finder(data_dir=data_dir)
    
    # For other datasets, load and subsample the data.
    u, x, t = data_load(dataset, data_dir=data_dir)
    u, x, t = subsample_data(u, x, t, spatial_factor=4, temporal_factor=4)
    
    # Case 2: NLS/Harmonic pipeline: use run_nls_finder.
    if dataset.lower() in ['nls', 'harmonic']:
        # print("Using NLS/harmonic pipeline...")
        dt = t[1] - t[0]
        # For the NLS pipeline, we assume different spatial indexing.
        dx = x[1] - x[0]
        return run_nls_finder(u, dt, dx)
    
    # Case 3: Default pipeline.
    print("Using default pipeline...")
    dt = t[1] - t[0]
    dx = x[2] - x[1]
    
    print("Building linear system...")
    Ut, R, rhs_des = build_linear_system(u, dt, dx, D=D, P=P, time_diff='FD', space_diff='FD')
    w = TrainSTRidge(R, Ut, 10**-5, 0.1)
    
    pde_str = print_and_save_pde(w, rhs_des, ut='u_t', file_path='discovered_pde.txt')
    candidate_terms = extract_terms_from_pde(pde_str)
    print("Extracted candidate terms:", candidate_terms)
    
    nonzero_idx = np.where(w != 0)
    R_candidate = R[:, nonzero_idx[0]]
    w_nonzero = w[nonzero_idx].flatten()
    print("Shape of R_candidate:", R_candidate.shape)
    print("Length of nonzero coefficients:", w_nonzero.shape[0])
    
    new_num_rows = 10000
    R_candidate_sub, Ut_sub = subsample_candidate_matrix(R_candidate, Ut, new_num_rows)
    print("Subsampled shape of R_candidate:", R_candidate_sub.shape)
    
    # Use the LLM to get initial coefficients.
    w_llm = llm_get_coefficients(candidate_terms, llm_name=llm_initial)
    print("LLM initial guess for coefficients:", w_llm)
    num_candidate = R_candidate.shape[1]
    if w_llm.shape[0] != num_candidate:
        print(f"Warning: LLM guess length ({w_llm.shape[0]}) does not match candidate columns ({num_candidate}).")
        print("Using STRidge nonzero coefficients as initial guess.")
        w_llm = w_nonzero
    
    # Get verified coefficients from the verification LLM.
    pde_name, w_verified = verify_llm(candidate_terms, llm_name=llm_verification)
    print("Verified coefficients from second LLM:", (pde_name, w_verified))
    w_llm = w_verified
    
    if w_llm.shape[0] != num_candidate:
        print(f"Warning: LLM guess length ({w_llm.shape[0]}) does not match candidate columns ({num_candidate}).")
        print("Using STRidge nonzero coefficients as initial guess.")
        w_llm = w_nonzero

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)
    
    R_candidate_torch = torch.tensor(np.real(R_candidate), dtype=torch.float32, device=device)
    Ut_torch = torch.tensor(np.real(Ut), dtype=torch.float32, device=device)
    
    w_param = torch.tensor(w_llm, dtype=torch.float32, device=device, requires_grad=True)
    optimizer = torch.optim.Adam([w_param], lr=1e-2)
    
    for epoch in range(num_epochs):
        optimizer.zero_grad()
        u_t_pred = torch.matmul(R_candidate_torch, w_param)
        loss = torch.mean((u_t_pred - Ut_torch)**2)
        loss.backward()
        optimizer.step()
        if epoch % 50 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")
    
    w_opt = w_param.detach().cpu().numpy().flatten()
    print("Optimized coefficients:", w_opt)
    final_mse = np.mean((np.real(R_candidate.dot(w_opt)) - np.real(Ut))**2)
    print("Optimized MSE:", final_mse)
    
    w_updated = np.zeros_like(w)
    w_updated[nonzero_idx] = w_opt.reshape(w_updated[nonzero_idx].shape)
    pde_str = print_and_save_pde_func_final(w_updated, rhs_des, candidate_terms, w_verified, ut='u_t', file_path='optimized_pde.txt')
    return w_updated, pde_str




if __name__ == "__main__":
    # For testing purposes, run with default parameters.
    run_pde_finder()
