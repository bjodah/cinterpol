# -*- coding: utf-8 -*-
__version__ = '0.3.3'

try:
    # Same naming convention as scipy.interpolate.
    from piecewise import Piecewise_poly as PiecewisePolynomial
except ImportError:
    # Enables setup.py to use model.py before
    # shared-object has been built
    pass
