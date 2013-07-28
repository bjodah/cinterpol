# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from cInterpol import interpolate_by_finite_diff

def test_interpolate_by_finite_diff():
    order = 0
    xarr = np.linspace(-1.5, 1.7, 53)
    xtest = np.linspace(-1.4, 1.6, 57)
    yarr = np.exp(xarr)
    for i in range(5):
        y = interpolate_by_finite_diff(xarr, yarr, xtest, order=i,
                                       ntail=5*(i+2), nhead=5*(i+2))
        print(i, '\n',y)
        #assert np.allclose(y, np.exp(xtest), atol=10**-(5-i), rtol=1e-3)

if __name__ == '__main__':
    test_interpolate_by_finite_diff()
