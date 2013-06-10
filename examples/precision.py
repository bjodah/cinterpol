#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for use with e.g. py.test
import numpy as np
import time
import matplotlib.pyplot as plt

from cInterpol import PiecewisePolynomial as cPiecewisePolynomial

from scipy.interpolate import PiecewisePolynomial

def main(start=0, stop=20, Ncoarse=21, Nfine=1000):
    """
    """
    x = np.linspace(start, stop, Ncoarse)
    y0 =  np.sin(x)
    y1 =  np.cos(x)
    y2 = -np.sin(x)
    all_y = np.ascontiguousarray(np.vstack((y0, y1, y2)).transpose())
    cpp = cPiecewisePolynomial(x, all_y)
    pp = PiecewisePolynomial(x, all_y)
    xfine = np.linspace(start, stop, Nfine)
    ipy = cpp(xfine)
    plt.subplot(3, 1, 1)
    plt.plot(x, y0, '*', label = 'Data')
    plt.plot(xfine, cpp(xfine), label='cInterpol')
    plt.plot(xfine, pp(xfine), label='SciPy PiecewisePolynomial')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(xfine, np.sin(xfine) - cpp(xfine), label='cInterpol analytic error')
    plt.subplot(3, 1, 3)
    plt.plot(xfine, pp(xfine) - cpp(xfine), label='cInterpol diff from scipy')
    plt.legend()

    plt.show()

if __name__ == '__main__':
    main()
