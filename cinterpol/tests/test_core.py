#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for use with e.g. py.test
import numpy as np
import matplotlib.pyplot as plt

from cinterpol import PiecewisePolynomial

try:
    import pytest
except ImportError:
    class pytest:
        class mark:
            class parametrize:
                def __init__(self, *args):
                    #self.kwargs = {args[i]: args[i + 1]}
                    pass
                def __call__(self, f):
                    def wrapper():
                        for kw in self.kws:
                            f(**kw)
                    return wrapper


t1 = np.array([0.0, 1.0])
y1 = np.array([[0.0, 0.0, 0.0],
              [1.0, 3.0, 6.0]]) # y=x**3
c1 = np.array(
        [[0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
         [1.0, 3.0, 6.0, 0.0, 0.0, 0.0]])
def f1(t):
    return t**3

t2 = np.array([1.0, 3.0])
y2 = np.array([[ 2.0,  5.0,  7.0],
               [11.0, 13.0, 17.0]]) # y=x**3
c2 = np.array(
    [[ 2.0, 5.0, 3.5, -10.25, 6.3125, -1.0625],
     [11.0,    13.0,    17.0,    0.0,    0.0,    0.0]])

def f2(t):
    return 18.125 -63.3125*t + 82.75*t**2 -46.125*t**3 + 11.625*t**4 -1.0625*t**5

arg_cases = [(t1,y1,c1,f1), (t2,y2,c2,f2)]

@pytest.mark.parametrize('args',  arg_cases)
def test_PiecewisePolynomial(args):
    t, y, c, f = args
    pw = PiecewisePolynomial(t, y)
    assert np.allclose(pw.get_t(), t)
    assert np.allclose(pw.get_c(), c)
    t_series = np.linspace(t[0], t[1], 50)
    interpol_y = pw(t_series)
    exact_y = f(t_series)
    assert np.allclose(exact_y, interpol_y)


def test_PiecewisePolynomial_call():
    pwpi=PiecewisePolynomial(np.array([0.0,1.0]),np.array([[0.0],[1.0]]))
    assert pwpi(0.5) == 0.5

if __name__ == '__main__':
    for args in arg_cases:
        test_PiecewisePolynomial(args)
    test_PiecewisePolynomial_call()

