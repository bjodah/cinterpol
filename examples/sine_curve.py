#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for use with e.g. py.test
import numpy as np
import matplotlib.pyplot as plt

import cPickle as pickle

from cInterpol import PiecewisePolynomial

pi7=21.991148575128552

def get_sin_pp(start=0, stop=pi7, Ncoarse=21):
    x = np.linspace(start, stop, Ncoarse)
    y0 =  np.sin(x)
    y1 =  np.cos(x)
    y2 = -np.sin(x)
    all_y = np.ascontiguousarray(np.vstack((y0, y1, y2)).transpose(),
                                 dtype=np.float64)
    return PiecewisePolynomial(x, all_y)

def get_cos_pp(start=0, stop=pi7, Ncoarse=21):
    x = np.linspace(start, stop, Ncoarse)
    y0 =  np.cos(x)
    y1 = -np.sin(x)
    y2 = -np.cos(x)
    all_y = np.ascontiguousarray(np.vstack((y0, y1, y2)).transpose(),
                                 dtype=np.float64)
    return PiecewisePolynomial(x, all_y)


def plot(pp, t0=None, tend=None, Nfine=4000, analytic_cb=np.sin,
         plot_rows=2, plot_cols=1, plot_idx=1, show=True):
    """
    """
    # Plot interpolation (extrapolation)
    t0 = t0 or pp.t[0]
    tend = tend or pp.t[-1]
    xfine = np.linspace(t0, tend, Nfine)
    plt.subplot(plot_rows, plot_cols, plot_idx)
    plt.plot(pp.t, pp.c[:,0], '*', label = 'Function evaluated points')
    plt.plot(xfine, pp(xfine), label='Interpolated')
    plt.plot(xfine, analytic_cb(xfine), label ='Analytic')
    plt.legend()

    plt.subplot(plot_rows, plot_cols, plot_idx+1)
    plt.plot(xfine, analytic_cb(xfine) - pp(xfine),
             label='Absolute error')
    plt.legend()
    if show: plt.show()


def minus_sin(x):
    return -np.sin(x)

def minus_cos(x):
    return -np.cos(x)

if __name__ == '__main__':
    pp = get_sin_pp()
    plot(pp, plot_rows=4, plot_cols=2, show=False)

    Dpp = pp.derivative()
    plot(Dpp, analytic_cb=np.cos, plot_rows=4, plot_cols=2,
         plot_idx=3, show=False)

    DDpp = pp.derivative(2)
    plot(DDpp, analytic_cb=minus_sin, plot_rows=4, plot_cols=2,
         plot_idx=5, show=False)

    DDDpp = pp.derivative(3)
    plot(DDDpp, analytic_cb=minus_cos, plot_rows=4, plot_cols=2,
         plot_idx=7, show=False)

    plt.show()
