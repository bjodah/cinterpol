# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)

__version__ = '0.3.5'

try:
    # Same naming convention as scipy.interpolate.
    from .piecewise import Piecewise_poly as PiecewisePolynomial
except ImportError:
    # Enables setup.py to use model.py before
    # shared-object has been built
    pass
