"""
Singleton config
"""

models = {
    'use_sympy': False,
    'use_old_model': False,
    'use_parallel_chainruns': True,
    'use_bounded_run': True,
    'default_chainruns_count': 2000,
    # __DEPRECATED__
    'chainruns_factor': 1000,

}

mh = {
    'trace_length': 1000,
}
