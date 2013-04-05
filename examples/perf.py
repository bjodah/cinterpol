#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for use with e.g. py.test
import numpy as np
import time
import matplotlib.pyplot as plt

from cinterpol import PiecewisePolynomial as cPiecewisePolynomial

from scipy.interpolate import PiecewisePolynomial

def get_scipy_pp(t,y):
    return PiecewisePolynomial(t,y)

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
    plt.plot(xfine, cpp(xfine), label='cinterpol')
    plt.plot(xfine, pp(xfine), label='SciPy PiecewisePolynomial')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(xfine, np.sin(xfine) - cpp(xfine), label='cInterpol analytic error')
    plt.subplot(3, 1, 3)
    plt.plot(xfine, pp(xfine) - cpp(xfine), label='cInterpol diff from scipy')
    plt.legend()

    plt.show()

def bench(start=0, stop=20, N=4e4):
    x = np.linspace(start, stop, N)
    y0 =  np.sin(x)
    y1 =  np.cos(x)
    y2 = -np.sin(x)
    all_y = np.ascontiguousarray(np.vstack((y0, y1, y2)).transpose())

    xfine=np.linspace(start,stop,N*3)
    cinterpol_start = time.time()
    cpp = cPiecewisePolynomial(x, all_y)
    cinterpol_res=cpp(xfine)
    cinterpol_stop = time.time()

    scipy_start = time.time()
    pp = PiecewisePolynomial(x, all_y)
    scipy_res=pp(xfine)
    scipy_stop = time.time()

    print 'cinterpol time: ', cinterpol_stop-cinterpol_start
    print 'scipy time:', scipy_stop - scipy_start

    print 'cinterpol err:',cinterpol_res[-5:]-np.sin(xfine[-5:])
    print 'scipy err:', scipy_res[-5:]-np.sin(xfine[-5:])

if __name__ == '__main__':
    main()
    bench()
