#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# for use with e.g. py.test
import numpy as np
import time
import matplotlib.pyplot as plt

from cInterpol import PiecewisePolynomial as cPiecewisePolynomial

from scipy.interpolate import PiecewisePolynomial

def bench(start=0, stop=20, N=1e6):
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

    # No check_nan
    cInterpol_no_check_nan_start = time.time()
    cpp = cPiecewisePolynomial(x, all_y, check_for_nan=False)
    cInterpol_no_check_nan_res=cpp(xfine)
    cInterpol_no_check_nan_stop = time.time()

    # No check_nan_monotone
    cInterpol_no_check_nan_monotone_start = time.time()
    cpp = cPiecewisePolynomial(x, all_y, check_for_nan=False,
                               ensure_strict_monotonicity=False)
    cInterpol_no_check_nan_monotone_res=cpp(xfine)
    cInterpol_no_check_nan_monotone_stop = time.time()


    scipy_start = time.time()
    pp = PiecewisePolynomial(x[:N/10000], all_y[:,:N/10000])
    scipy_res=pp(xfine)
    scipy_stop = time.time()

    scipy_time = (scipy_stop - scipy_start)*10000
    print('scipy extrapolated time:', scipy_time)

    cInterpol_time = cInterpol_stop-cInterpol_start
    print('cInterpol time/speedup: ', cInterpol_time, scipy_time/cInterpol_time)

    cInterpol_no_check_nan_time = cInterpol_no_check_nan_stop -\
                                  cInterpol_no_check_nan_start
    print('cInterpol time/speedup (without check_nan): ',
          cInterpol_no_check_nan_time, scipy_time/cInterpol_no_check_nan_time)

    cInterpol_no_check_nan_monotone_time = cInterpol_no_check_nan_monotone_stop -\
                                  cInterpol_no_check_nan_monotone_start
    print('cInterpol time/speedup (without check_nan/check_strict_monotonicity): ',
          cInterpol_no_check_nan_monotone_time,
          scipy_time/cInterpol_no_check_nan_monotone_time)

    print('cInterpol err:',cInterpol_res[-5:]-np.sin(xfine[-5:]))
    print('scipy err:', scipy_res[-5:]-np.sin(xfine[-5:]))

if __name__ == '__main__':
    print('This can take up to a minute...')
    bench()
