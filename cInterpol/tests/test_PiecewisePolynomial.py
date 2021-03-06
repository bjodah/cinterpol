#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import pytest
import numpy as np

from cInterpol import PiecewisePolynomial
from cInterpol.model import Polynomial

t1 = np.array([0.0, 1.0])
y1 = np.array([[0.0, 0.0, 0.0],
              [1.0, 3.0, 6.0]]) # y=x**3

t2 = np.array([1.0, 3.0])
y2 = np.array([[ 2.0,  5.0,  7.0],
               [11.0, 13.0, 17.0]]) # y=f2(t)


t3 = np.array([1.0, 3.0, 23.0, 29.0])
y3 = np.array([[ 2.0,  5.0,  7.0],
               [43.0, 51.0, 53.0],
               [11.0, 13.0, 17.0],
               [101.0, 31.0, 37.0]]) # y=f2(t)


arg_cases = [(t1,y1), (t2,y2), (t3,y3)]


@pytest.mark.parametrize('args',  arg_cases)
def test_PiecewisePolynomial(args):
    t, y = args # t,y,c,f
    pw = PiecewisePolynomial(t, y)
    assert np.allclose(pw.t, t)

    # Let's determine the derivatives at
    # the points from the coefficients and
    # compare with y
    for ri, row in enumerate(pw.c):
        nc = y.shape[1]
        poly = Polynomial(c=row)
        if ri==pw.c.shape[0]-1:
            # Last
            ref = np.array([poly.eval(0, i) for i in range(nc)], dtype=np.float64)
            assert np.allclose(y[ri, :], ref)

            ref = np.array([poly.eval(t[ri-1]-t[ri], i) for i in range(nc)], dtype=np.float64)
            assert np.allclose(y[ri-1, :], ref)
        else:
            # Not last
            ref = np.array([poly.eval(0, i) for i in range(nc)], dtype=np.float64)
            assert np.allclose(y[ri, :], ref)

            ref = np.array([poly.eval(t[ri+1]-t[ri], i) for i in range(nc)], dtype=np.float64)
            assert np.allclose(y[ri+1, :], ref)


def test_PiecewisePolynomial_call():
    # y = x
    pwpi=PiecewisePolynomial(np.array([0.0,1.0]),
                             np.array([[0.0],[1.0]]))
    assert pwpi(-1.5) == -1.5
    assert pwpi(0.5) == 0.5
    assert pwpi(1.5) == 1.5

    assert pwpi(-1.5, deriv=1) == 1.0
    assert pwpi(-1.0, deriv=1) == 1.0
    assert pwpi( 0.0, deriv=1) == 1.0
    assert pwpi( 0.5, deriv=1) == 1.0
    assert pwpi( 1.0, deriv=1) == 1.0
    assert pwpi( 1.5, deriv=1) == 1.0


if __name__ == '__main__':
    test_PiecewisePolynomial_call()
    for args in arg_cases:
        test_PiecewisePolynomial(args)
    print("{} {}".format(__file__, 'passed'))
    sys.exit(0)
