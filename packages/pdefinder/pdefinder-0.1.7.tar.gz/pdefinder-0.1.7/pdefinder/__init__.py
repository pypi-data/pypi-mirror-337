# __init__.py
from .core import (
    data_load,
    subsample_data,
    build_linear_system,
    TrainSTRidge,
    print_and_save_pde,
    print_and_save_pde_func_final,
    extract_terms_from_pde,
    llm_get_coefficients,
    verify_llm,
    run_ns_finder,
    run_nls_finder,
    run_pde_finder # the main pipeline function
)

