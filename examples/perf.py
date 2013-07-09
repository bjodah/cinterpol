#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# for use with e.g. py.test
import numpy as np
import time
import matplotlib.pyplot as plt

from cInterpol import PiecewisePolynomial as cPiecewisePolynomial

from scipy.interpolate import PiecewisePolynomial

def bench(start=0, stop=20, N=4e4):
    x = np.linspace(start, stop, N)
    y0 =  np.sin(x)
    y1 =  np.cos(x)
    y2 = -np.sin(x)
    all_y = np.ascontiguousarray(np.vstack((y0, y1, y2)).transpose())

    xfine=np.linspace(start,stop,N*3)
    cInterpol_start = time.time()
    cpp = cPiecewisePolynomial(x, all_y)
    cInterpol_res=cpp(xfine)
    cInterpol_stop = time.time()

    cInterpol_no_check_start = time.time()
    cpp = cPiecewisePolynomial(x, all_y, check_nan=False)
    cInterpol_no_check_res=cpp(xfine)
    cInterpol_no_check_stop = time.time()

    scipy_start = time.time()
    pp = PiecewisePolynomial(x, all_y)
    scipy_res=pp(xfine)
    scipy_stop = time.time()

    scipy_time = scipy_stop - scipy_start
    print('scipy time:', scipy_time)

    cInterpol_time = cInterpol_stop-cInterpol_start
    print('cInterpol time/speedup: ', cInterpol_time, scipy_time/cInterpol_time)

    cInterpol_no_check_time = cInterpol_no_check_stop-cInterpol_no_check_start
    print('cInterpol time/speedup (without checking for NaN): ', cInterpol_no_check_time, scipy_time/cInterpol_no_check_time)

    print('cInterpol err:',cInterpol_res[-5:]-np.sin(xfine[-5:]))
    print('scipy err:', scipy_res[-5:]-np.sin(xfine[-5:]))

if __name__ == '__main__':
    print('This can take a minute or two...')
    bench()
