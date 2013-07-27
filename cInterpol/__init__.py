try:
    from core import PiecewisePolynomial
    from finitediff_wrapper import interpolate_by_finite_diff
except ImportError:
    # Enables setup.py to use poly_coeff_expr.py before
    # shared-object has been built
    pass
