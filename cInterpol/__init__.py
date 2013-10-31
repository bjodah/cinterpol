try:
    from core import Piecewise_poly as PiecewisePolynomial
    from core import interpolate_by_finite_diff
except ImportError:
    import sys
    if sys.argv[0].endswith('setup.py'):
        # Enables setup.py to use setup.py before
        # shared-objects have been built
        pass
    else:
        raise
