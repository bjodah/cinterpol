# -*- coding: utf-8 -*-
import numpy as np
cimport numpy as cnp
from cpython cimport bool
from newton_interval cimport get_interval, get_interval_from_guess, check_nan, check_strict_monotonicity

# Note: Cython >=0.19 support const properly.


%for token in tokens:
%for wy in range(1,max_wy+1):

cdef extern void ${token}_coeff${wy}(const double * const t,
                                     const double * const y,
                                     double * const c,
                                     const ${SIZE_T} nt) nogil

%for i in range(max_deriv[wy]+1):

cdef extern double ${token}_scalar_${wy}_${i}(
    const double t, const double * const c, const ${SIZE_T} offset) nogil

cdef extern void ${token}_eval_${wy}_${i}(
    const ${SIZE_T} nt,
    const double * const t,
    const double * const c,
    const ${SIZE_T} nout,
    const double * const tout,
    double * const yout,
) nogil

%endfor
%endfor
%endfor


cdef bint has_nan(double * arr, int n) nogil:
    return check_nan(arr, n) != -1 # if no NaN, -1 is returned

cdef bint obeys_strict_monotonicity(double * arr, int n) nogil:
    return check_strict_monotonicity(arr, n) == 1

cdef int _get_index(double [:] tarr, double tgt, bint allow_extrapol, int guess = -1):
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
        if guess == -1:
            return get_interval(&tarr[0], tarr.size, tgt)
        else:
            return get_interval_from_guess(
                &tarr[0], tarr.size, tgt, guess)


%for token in tokens:
cpdef Piecewise_${token} Piecewise_${token}_from_coefficients(
    double [::1] t, double[:, ::1] c, allow_extrapol=True):
    # Classmethods not supported by cdef extension types,
    # this is a proxy function
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


    def __cinit__(self, double [::1] t, double [:,::1] y, _c = None,
                  allow_extrapol=True, check_for_nan=True,
                  ensure_strict_monotonicity=True):
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
            if self.wy < 1 or self.wy > ${max_wy}:
                raise ValueError('Invlid wy: {}'.format(self.wy))
          %for i in range(1, max_wy+1):
            elif self.wy == ${i}:
                ${token}_coeff${i}(&t[0], &y[0,0], &c[0,0], len(t))
          %endfor
            self.t = t
            self.c = c

        if check_for_nan:
            if has_nan(&self.t[0], len(self.t)):
                raise ValueError('NaN encountered!')
            if has_nan(&self.c[0,0], self.c.shape[0]*self.c.shape[1]):
                raise ValueError('NaN encountered!')
        if ensure_strict_monotonicity:
            if not obeys_strict_monotonicity(&self.t[0], len(self.t)):
                raise ValueError('Not monotone!')


    def __call__(self, t, int deriv = 0):
        # First 3 are used only in the case of t is float
        cdef double y
        cdef ${SIZE_T} it
        cdef int j
        cdef cnp.ndarray[cnp.float64_t, ndim=1] yout
        cdef cnp.ndarray[cnp.float64_t, ndim=1] tout

        if isinstance(t, np.ndarray):
            tout = np.ascontiguousarray(t)
        else:
            if isinstance(t, int): t = float(t)
            if isinstance(t, float):
                it = _get_index(self.t, t, True)
                if self.wy < 1 or self.wy > ${max_wy}:
                    raise ValueError('Invlid wy: {}'.format(self.wy))
              %for wy in range(1, max_wy+1):
                elif self.wy == ${wy}:
                    if deriv < 0 or deriv > ${max_deriv[wy]}:
                        raise ValueError(
                            "Invalid derivative: {}".format(deriv))
                  %for i in range(max_deriv[wy]+1):
                    elif deriv == ${i}:
                        y = ${token}_scalar_${wy}_${i}(
                            t - self.t[it], &self.c[0, 0], it*${wy}*2)
                  %endfor
              %endfor
                return np.array(y, dtype = np.float64)
            tout = np.array(t, dtype=np.float64)

        yout = np.empty_like(tout)

        if self.wy < 1 or self.wy > ${max_wy}:
            raise ValueError('Invlid wy: {}'.format(self.wy))
      %for wy in range(1, max_wy+1):
        elif self.wy == ${wy}:
            if deriv < 0 or deriv > ${max_deriv[wy]}:
                raise ValueError("Invalid derivative: {}".format(deriv))
          %for i in range(max_deriv[wy]+1):
            elif deriv == ${i}:
                ${token}_eval_${wy}_${i}(
                    self.t.size, &self.t[0], &self.c[0,0],
                    tout.size, &tout[0], &yout[0])
          %endfor
      %endfor

        return yout


    def __reduce__(self):
        return Piecewise_${token}_from_coefficients, (
            np.asarray(self.t), np.asarray(self.c),
            self.allow_extrapol)

%endfor
