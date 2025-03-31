import argparse
from pdefinder import run_pde_finder

def main():
    parser = argparse.ArgumentParser(description="Run PDE discovery pipeline.")
    parser.add_argument('--dataset', type=str, default='KS', help="Dataset name (e.g., 'KS', 'Burgers', 'NS')")
    parser.add_argument('--data_dir', type=str, default=".", help="Directory for dataset files")
    # parser.add_argument('--pde_type', type=str, default='default', help="Type of PDE pipeline: 'default', 'nls', or 'harmonic'")
    parser.add_argument('--P', type=int, default=5, help="Max polynomial power (default pipeline)")
    parser.add_argument('--D', type=int, default=5, help="Max derivative order (default pipeline)")
    parser.add_argument('--epochs', type=int, default=1000, help="Number of optimization epochs")
    parser.add_argument('--llm_initial', type=str, default='default_llm', help="LLM for initial coefficient guess")
    parser.add_argument('--llm_verification', type=str, default='default_llm', help="LLM for verification")
    args = parser.parse_args()
    
    run_pde_finder(dataset=args.dataset, P=args.P, D=args.D, num_epochs=args.epochs, 
                   data_dir=args.data_dir, pde_type=args.pde_type,
                   llm_initial=args.llm_initial, llm_verification=args.llm_verification)

if __name__ == "__main__":
    main()
