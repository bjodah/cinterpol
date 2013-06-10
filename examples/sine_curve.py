#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for use with e.g. py.test
import numpy as np
import matplotlib.pyplot as plt

import cPickle as pickle

from cInterpol import PiecewisePolynomial

def get_sin_pp(start=0, stop=20, Ncoarse=21):
    x = np.linspace(start, stop, Ncoarse)
    y0 =  np.sin(x)
    y1 =  np.cos(x)
    y2 = -np.sin(x)
    all_y = np.ascontiguousarray(np.vstack((y0, y1, y2)).transpose(),dtype=np.float64)
    return PiecewisePolynomial(x, all_y)

def plot(pp, t0=None, tend=None, Nfine=1000):
    """
    """
    # Plot interpolation (extrapolation)
    t0 = t0 or pp.t[0]
    tend = tend or pp.t[-1]
    xfine = np.linspace(t0, tend, Nfine)
    plt.subplot(2, 1, 1)
    plt.plot(pp.t, pp.c[:,0], '*', label = 'Function evaluated points')
    plt.plot(xfine, pp(xfine), label='Interpolated')
    plt.plot(xfine, np.sin(xfine), label ='Analytic')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(xfine, np.sin(xfine) - pp(xfine), label='Absolute error')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    pp = get_sin_pp()
    plot(pp)
