try:
    from core import PiecewisePolynomial, interpolate_by_finite_diff, derivatives_at_point_by_finite_diff
except ImportError:
    # Enables setup.py to use poly_coeff_expr.py before
    # shared-object has been built
    pass
