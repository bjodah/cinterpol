# -*- coding: utf-8 -*-
import numpy as np
cimport numpy as cnp
from cpython cimport bool
from newton_interval cimport get_interval

# Note: Cython >=0.19 support const properly.


%for token in tokens:
%for i in range(1,max_wy+1):

cdef extern void ${token}_eval_${wy}(int nt,
                              int wy,
                              double * t,
                              double * c,
                              int nout,
                              double * tout,
                              double * yout,
                              int derivative
                          )

cdef extern int ${token}_scalar_${wy}(double t,
                                double * c,
                                int derivative
                          )

cdef extern void ${token}_coeff_${i}(const double t[], const double y[], double c[], const size_t nt)

%endfor
%endfor


cdef bint _check_nan(double * arr, int n) nogil:
    cdef double x
    cdef int i

    for i in range(n):
        x = arr[i]
        if x != x:
            return False
    return True


cdef bint _check_strict_monotonicity(double * arr, int n) nogil:
    cdef double x, old_x
    cdef int i

    old_x = arr[0]
    for i in range(1,n):
        x = arr[i]
        if x <= old_x:
            return False
        old_x = x
    return True


cdef int _get_index(double [:] tarr, double tgt, bint allow_extrapol):
        if tgt < tarr[0]:
            if allow_extrapol == True:
                return 0
            else:
                raise ValueError(
                    'Out of bounds (allow_extrapol set to False)')
        elif tgt > tarr[-1]:
            if allow_extrapol == True:
                return tarr.size-1
            else:
                raise ValueError(
                    'Out of bounds (allow_extrapol set to False)')
        else:
            return get_interval(&tarr[0], tarr.size, tgt)



%for token in tokens
cpdef Piecewise_${token} Piecewise_${token}_from_coefficients(
    t, c, allow_extrapol=True):
    # Classmethods not supported by cdef extension types,
    # this is a proxy function
    t = np.ascontiguousarray(t)
    c = (c)
    return Piecewise_${token}(t, c, c, allow_extrapol)

cdef class Piecewise_${token}:
    """
    for `poly`: mimics PiecewisePolynomial class
    (mimics scipy.interpolate.PiecewisePolynomial)
    """
    cdef public double [:] t
    cdef public double [:,:] c
    cdef public int wy # width of y matrix (# of deriv per y incl 0th)
    cdef public bool allow_extrapol


    def __cinit__(self, double [:] t, double [:,:] y, _c = None,
                  allow_extrapol=True, check_nan=True,
                  check_strict_monotonicity=True):
        """ Sets t, c and wy"""
        cdef cnp.ndarray[cnp.float64_t, ndim=2] c = \
            np.ascontiguousarray(np.empty((y.shape[0], y.shape[1] * 2),
                                          dtype = np.float64))
        if _c != None:
            # init from t and c
            self.t = np.ascontiguousarray(t)
            self.c = np.ascontiguousarray(_c)
            self.wy = _c.shape[1] / 2
            self.allow_extrapol = allow_extrapol
        else:
            # init from t and y
            t = np.ascontiguousarray(t)
            y = np.ascontiguousarray(y)

            self.allow_extrapol = allow_extrapol
            self.wy = y.shape[1]
            if self.wy == 1:
                ${token}_coeff_1(&t[0], &y[0,0], &c[0,0], len(t))
%for i in range(2, max_wy+1):
            elif self.wy == ${i}:
                ${token}_coeff_${i}(&t[0], &y[0,0], &c[0,0], len(t))
%endfor

            self.t = t
            self.c = c

        if check_nan:
            if not _check_nan(&self.t[0], len(self.t)):
                raise ValueError('NaN encountered!')
            if not _check_nan(
                    &self.c[0,0], self.c.shape[0]*self.c.shape[1]):
                raise ValueError('NaN encountered!')
        if check_strict_monotonicity:
            if not _check_strict_monotonicity(&self.t[0], len(self.t)):
                raise ValueError('Not monotone!')


    def __call__(self, t, int deriv = 0):
        # First 3 are used only in the case of t is float
        cdef double y
        cdef size_t it
        cdef int j
        cdef cnp.ndarray[cnp.float64_t, ndim=1] yout
        cdef cnp.ndarray[cnp.float64_t, ndim=1] tout

        assert deriv <= ${max_deriv}
        if isinstance(t, np.ndarray):
            tout = np.ascontiguousarray(t)
        else:
            if isinstance(t, float):
                y = 0.0
                it = _get_index(self.t, t, True)
                y = ${token}_scalar(t - self.t[it], &self.c[it, 0],
                                    deriv)
                return np.array(y, dtype = np.float64)
            tout = np.array(t, dtype=np.float64)

        yout = np.empty_like(tout)

        if self.wy == 1:
            ${token}_eval_1(
                self.t.size, self.wy, &self.t[0],
                &self.c[0,0], tout.size, &tout[0],
                &yout[0], deriv)
        %for i in range(2, max_wy+1):
        elif self.wy == ${i}:
            ${token}_eval_${wy}(
                self.t.size, self.wy, &self.t[0],
                &self.c[0,0], tout.size, &tout[0], &yout[0], deriv)
        %endfor

        return yout


    # def derivative(self, int nth=1):
    #     if nth == 0:
    #         return self
    #     if nth == 1:
    #         assert self.wy >= 1
    #         new_c = self.c[:,1:]*np.arange(1, self.wy*2).reshape(
    #             (1, self.wy*2-1))
    #         return Piecewise_${token}_from_coefficients(
    #             self.t, new_c, allow_extrapol=self.allow_extrapol)
    #     elif nth > 1:
    #         # recursive solution
    #         assert nth <= self.wy*2-1
    #         return self.derivative(1).derivative(nth-1)
    #     else:
    #         raise ValueError("That would be the integral?")


    def __reduce__(self):
        return Piecewise_${token}_from_coefficients, (
            np.asarray(self.t), np.asarray(self.c),
            self.allow_extrapol)
