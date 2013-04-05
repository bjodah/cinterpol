import numpy as np
cimport numpy as np
#from libc.math cimport pow as c_pow

# Cython 0.19-dev support const properly since 2013-03-26

cdef extern size_t get_interval(const double arr[], const size_t N, const double t)
cdef extern void poly_coeff1(const double t[], const double y[], double c[], const size_t nt)
cdef extern void poly_coeff3(const double t[], const double y[], double c[], const size_t nt)
cdef extern void poly_coeff5(const double t[], const double y[], double c[], const size_t nt)


cdef ensure_contiguous(arr):
    if isinstance(arr, np.ndarray):
        if arr.flags.c_contiguous:
            return arr
        else:
            return np.ascontiguousarray(arr)
    else:
        return np.ascontiguousarray(arr)


cpdef PiecewisePolynomial PiecewisePolynomial_from_coefficients(t, c):
    t = ensure_contiguous(t)
    c = ensure_contiguous(c)
    return PiecewisePolynomial(t, c, c)



cdef class PiecewisePolynomial:
    """
    PiecewisePolynomial class (mimics scipy.interpolate.PiecewisePolynomial)
    """
    cdef double [:] t
    cdef double [:,:] c
    cdef int order

    def __cinit__(self, double [:] t, double [:,:] y, _c = None):
        if _c != None:
            self.t = ensure_contiguous(t)
            self.c = ensure_contiguous(_c)
            return

        cdef np.ndarray[np.float64_t, ndim=2] c = np.ascontiguousarray(np.empty(
            (y.shape[0], y.shape[1] * 2), dtype = np.float64))

        t = ensure_contiguous(t)
        y = ensure_contiguous(y)

        self.order = y.shape[1] - 1
        if self.order == 0:
            poly_coeff1(&t[0], &y[0,0], &c[0,0], len(t))
        elif self.order == 1:
            poly_coeff3(&t[0], &y[0,0], &c[0,0], len(t))
        elif self.order == 2:
            poly_coeff5(&t[0], &y[0,0], &c[0,0], len(t))

        self.t = t
        self.c = c

    def __call__(self, t):
        # These 3 are used in case of t is float
        cdef double y
        cdef size_t it
        cdef int j
        cdef double [:] yout
        if isinstance(t, np.ndarray):
            if not t.flags.c_contiguous:
                t = np.ascontiguousarray(t)
        else:
            if isinstance(t, float):
                y = 0.0
                if self.t[0] <= t and t <= self.t[-1]:
                    it = get_interval(&self.t[0], len(self.t), t)
                else:
                    raise ValueError('Out of bounds')
                for j in range((self.order + 1)*2):
                    y += (t - self.t[it]) ** j * self.c[it, j]
                return np.array(y, dtype = np.float64)
            t = np.array(t, dtype=np.float64)
        yout = np.ascontiguousarray(np.empty(t.shape, dtype=np.float64))
        self._interpol(t, yout)
        return np.asarray(yout)

    cdef _interpol(self,
                   double [:] t,
                   double [:] yout):
        """
        Modify `yout` inplace to store interpolated values at `t`
        """
        cdef size_t i = 0
        cdef size_t it
        cdef int j
        cdef size_t t_size = len(t)
        cdef double y
        if self.t[0] <= t[0] and t[-1] <= self.t[-1]:
            it  = get_interval(&self.t[0], len(self.t), t[0])
        else:
            raise ValueError('Out of bounds')

        while i < t_size:
            if t[i] > self.t[it + 1]:
                it += 1
                continue
            y = 0.0
            for j in range((self.order + 1)*2):
                y += (t[i] - self.t[it]) ** j * self.c[it, j]
            yout[i] = y
            i += 1

    def __reduce__(self):
        return PiecewisePolynomial_from_coefficients, (np.asarray(self.t), np.asarray(self.c))

    def get_c(self):
        return np.asarray(self.c)

    def get_t(self):
        return np.asarray(self.t)
