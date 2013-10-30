# -*- coding: utf-8 -*-
cimport numpy as cnp
from newton_interval cimport get_interval

import numpy as np

cdef extern void apply_fd(int * nin, int * maxorder, double * xdata, double * ydata, double * xtgt, double * out)

cdef extern void populate_weights(double * z, double * x, int * nd,
                                  int * m, double * c)

cdef bint is_equidistant(double [:] x, double abstol=1e-9,
                         double reltol=1e-9):
    cdef int i
    cdef double dx
    cdef double rdx = x[1]-x[0] # ref dx
    if rdx == 0.0:
        return False
    for i in range(2,x.shape[0]):
        dx = x[i]-x[i-1]
        if abs(rdx-dx) > abstol or abs(dx/rdx-1.0) > reltol:
            return False
    return True


def interpolate_by_finite_diff(double [:] xdata, double [:] ydata,
                               double [:] xout, int maxorder=0,
                               int ntail=2, int nhead=2):
    """
    Interpolates function value (or its derivative - `order`)
    at xout based on finite difference using provided xdata and
    ydata. Algortithm assumes non-regularly spaced xdata. If
    xdata is regularly spaced this algortihm is not the optimal
    to use with respect to performance.

    The underlying algorithm (here implemented in C) is from:
    Generation of Finite Difference Formulas on Arbitrarily
        Spaced Grids, Bengt Fornberg
    Mathematics of compuation, 51, 184, 1988, 699-706
    """
    cdef cnp.ndarray[cnp.float64_t, ndim=1] xdata_arr = \
        np.ascontiguousarray(xdata)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] ydata_arr = \
        np.ascontiguousarray(ydata)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] xout_arr = \
        np.ascontiguousarray(xout)
    cdef int nin = ntail+nhead
    cdef int nout = xout.shape[0]
    cdef cnp.ndarray[cnp.float64_t, ndim=1] out = np.zeros(maxorder+1)
    cdef cnp.ndarray[cnp.float64_t, ndim=2] yout = \
        np.zeros((nout, maxorder+1), order='C')
    cdef int i,j # i,j are counters
    cdef double xtgt

    assert xdata_arr.shape[0] >= ntail+nhead
    assert xdata_arr.shape[0] == ydata_arr.shape[0]
    assert nhead+ntail >= maxorder+1

    for i in range(nout):
        xtgt=xout[i]
        j = max(0, get_interval(
            &xdata_arr[0],xdata_arr.shape[0], xtgt))
        j = min(j, xdata_arr.shape[0]-nin)
        apply_fd(&nin,
                 &maxorder,
                 &xdata_arr[j],
                 &ydata_arr[j],
                 &xtgt,
                 <double *>out.data)
        yout[i,:] = out
    return yout


# cdef get_weights(double [:] xarr, double xtgt, int n, int maxorder=0):
#     cdef cnp.ndarray[cnp.float64_t, ndim=2, mode='fortran'] c = \
#         np.zeros((n, maxorder+1), order='F')
#     cdef int nm1 = n-1 # n minus 1
#     populate_weights(&xtgt, &xarr[0], &nm1, &maxorder, &c[0,0])
#     return c
