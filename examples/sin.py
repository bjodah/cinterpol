#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for use with e.g. py.test
import numpy as np
import matplotlib.pyplot as plt

import cPickle as pickle

from cinterpol import PiecewisePolynomial

def main(start=0, stop=20, Ncoarse=21, Nfine=1000, save=None, pp=None):
    """
    """
    x = np.linspace(start, stop, Ncoarse)
    y0 =  np.sin(x)
    if not pp:
        y1 =  np.cos(x)
        y2 = -np.sin(x)
        all_y = np.ascontiguousarray(np.vstack((y0, y1, y2)).transpose(),dtype=np.float64)
        pp = PiecewisePolynomial(x, all_y)

    # Plot interpolation
    xfine = np.linspace(start, stop, Nfine)
    plt.subplot(2, 1, 1)

    plt.plot(x, y0, '*', label = 'Data')
    plt.plot(xfine, pp(xfine), label='Interpolated')
    plt.plot(xfine, np.sin(xfine), label ='Analytic')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(xfine, np.sin(xfine) - pp(xfine), label='Error')
    plt.legend()
    plt.show()

    # Demo serialization
    if save:
        ori_t, ori_c = pp.get_t(), pp.get_c()
        pickle.dump(pp, open(save, 'wb'))#, protocol = 2)
        pp2 = pickle.load(open(save, 'rb'))
        assert np.allclose(pp2.get_t(), ori_t) and \
               np.allclose(pp2.get_c(), ori_c)


if __name__ == '__main__':
    main(save='pp.pkl')
    pp_loaded = pickle.load(open('pp.pkl', 'rb'))
    main(pp=pp_loaded)

