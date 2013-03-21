#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for use with e.g. py.test
import numpy as np
import matplotlib.pyplot as plt

from cinterpol import PieceWisePolyInterpol

def main(start=0, stop=20, Ncoarse=20, Nfine=1000):
    """
    """
    x = np.linspace(start, stop, Ncoarse)
    y0 =  np.sin(x)
    y1 =  np.cos(x)
    y2 = -np.sin(x)
    all_y = np.ascontiguousarray(np.vstack((y0, y1, y2)).transpose())
    print all_y.shape
    pw = PieceWisePolyInterpol(x, all_y)

    xfine = np.linspace(start, stop, Nfine)
    ipy = pw(xfine)

    plt.plot(x, y0, '*', label = 'Data')
    plt.plot(xfine, ipy, label='Interpolated')
    plt.plot(xfine, np.sin(xfine), label ='Analytic')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
