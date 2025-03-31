Below is a description of our package


`pdefinder` is a Python package for discovering partial differential equations (PDEs) from data using data-driven techniques. The package implements methods inspired by PDE-FIND and includes utilities for building candidate libraries, computing numerical derivatives, performing sparse regression, and optimizing candidate coefficients. 

## Features

- **Candidate Library Construction:** Build a library of candidate PDE terms using polynomial functions and numerical differentiation.
- **Numerical Differentiation:** Compute derivatives using finite differences, polynomial interpolation, or Tikhonov regularization.
- **Sparse Regression Methods:** Available techniques include STRidge, Lasso, ElasticNet, and FoBa.
- **Data Subsampling:** Easily subsample data along spatial and temporal dimensions.
- **LLM Integration:** Interface with language models (via the OpenAI API) for initial coefficient estimation and verification.
- **Optimization:** Utilize CUDA-enabled PyTorch for efficient optimization of PDE coefficients.

## Installation

Clone the repository and install the package locally:

```bash
git clone https://github.com/Amartya-Roy/pdefinder.git
cd pdefinder
pip install .
```

Alternatively, build the package distribution and install:

```bash
python setup.py sdist bdist_wheel
pip install dist/pdefinder-0.1.0-py3-none-any.whl
```

## Usage

### Command-Line Interface

You can run the PDE discovery pipeline from the command line. For example:

```bash
pdefinder --dataset KS --data_dir /path/to/data --P 5 --D 5 --epochs 1000
```

  
### Python API

Import and run the main function in your own script:

```python
from pdefinder import run_pde_finder

# Run the PDE discovery pipeline with custom parameters.
w_final, pde_expression = run_pde_finder(
    dataset='KS',
    P=5,
    D=5,
    num_epochs=1000,
    data_dir='/path/to/data',      
    llm_initial='my_llm',         # Identifier for the initial LLM
    llm_verification='my_llm'     # Identifier for the verification LLM
)

print("Optimized Coefficients:", w_final)
print("Discovered PDE:", pde_expression)
```

### Parameters

- **dataset**: The dataset to use.(`.mat` or `.npy` format)
- **P**: Maximum polynomial power to include in the candidate library (default pipeline).
- **D**: Maximum derivative order to include (default pipeline).
- **num_epochs**: Number of epochs for the PyTorch optimization step (default pipeline).
- **data_dir**: Directory where the dataset files are located.
- **llm_initial**: Identifier for the language model used to generate initial coefficient guesses.
- **llm_verification**: Identifier for the language model used for verification.

## Dependencies

The package requires:
- Python 3.6 or higher
- [numpy](https://numpy.org/)
- [scipy](https://www.scipy.org/)
- [torch](https://pytorch.org/)
- [openai](https://github.com/openai/openai-python)

Install the dependencies using pip:

```bash
pip install numpy scipy torch openai
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub for any bug reports, feature requests, or improvements.

## Acknowledgments

This package is inspired by recent advances in data-driven PDE discovery methods. Special thanks to `Soumya Mallick` who helped me thinking about this idea.

## Repository

For more information, visit the GitHub repository:  
[https://github.com/Amartya-Roy/pdefinder](https://github.com/Amartya-Roy/pdefinder)
```
