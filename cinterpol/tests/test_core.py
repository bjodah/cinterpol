#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for use with e.g. py.test
import numpy as np
import matplotlib.pyplot as plt

from cinterpol import PieceWisePolyInterpol


def test_PieceWisePolyInterpol_mk_from_data():
    t = np.array([0.0, 1.0])
    y = np.array([[0.0, 0.0, 0.0],
                  [1.0, 3.0, 6.0]]) # y=x**3
    t = PieceWisePolyInterpol.mk_from_data(t, y)
    assert np.allclose(t.get_t(), t)
    assert np.allclose(t.get_c(), np.array(
        [[0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
         [1.0, 3.0, 6.0, 0.0, 0.0, 0.0]]))
    t_series = np.linspace(0, 1.0, 50)
    interpol_y = t(t_series)
    exact_y = t_series ** 3
    assert np.allclose(exact_y, interpol_y)

