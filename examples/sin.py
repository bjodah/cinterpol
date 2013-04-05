#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for use with e.g. py.test
import numpy as np
import matplotlib.pyplot as plt

import cPickle as pickle

from cinterpol import PiecewisePolynomial

def main(start=0, stop=20, Ncoarse=21, Nfine=1000):
    """
    """
    x = np.linspace(start, stop, Ncoarse)
    y0 =  np.sin(x)
    y1 =  np.cos(x)
    y2 = -np.sin(x)
    all_y = np.ascontiguousarray(np.vstack((y0, y1, y2)).transpose())
    pw = PiecewisePolynomial(x, all_y)

    # Demo serialization
    f,data = pw.__reduce__()
    print f(*data)
    pickle.dump(pw, open('pw.pkl', 'wb'))#, protocol = 2)
    del pw
    pw = pickle.load(open('pw.pkl', 'rb'))

    # Plot interpolation
    xfine = np.linspace(start, stop, Nfine)
    plt.subplot(2, 1, 1)

    plt.plot(x, y0, '*', label = 'Data')
    plt.plot(xfine, pw(xfine), label='Interpolated')
    plt.plot(xfine, np.sin(xfine), label ='Analytic')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(xfine, np.sin(xfine) - pw(xfine), label='Error')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
