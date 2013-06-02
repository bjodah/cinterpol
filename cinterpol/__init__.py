try:
    from core import PiecewisePolynomial
except ImportError:
    # Enables setup.py to use poly_coeff_expr.py before shared-object core has been built
    pass
