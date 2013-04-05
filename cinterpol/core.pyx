import numpy as np
cimport numpy as np

# Cython 0.19-dev support const properly since 2013-03-26

cdef extern size_t get_interval(const double arr[], const size_t N, const double t)
cdef extern void poly_coeff1(const double t[], const double y[], double c[], const size_t nt)
cdef extern void poly_coeff3(const double t[], const double y[], double c[], const size_t nt)
cdef extern void poly_coeff5(const double t[], const double y[], double c[], const size_t nt)

cpdef PiecewisePolynomial PiecewisePolynomial_from_coefficients(t, c):
    cdef PiecewisePolynomial instance = PiecewisePolynomial.__new__(PiecewisePolynomial)
    t = np.ascontiguousarray(t)
    c = np.ascontiguousarray(c)

    if c.ndim == 1:
        c = np.ascontiguousarray(c.reshape((len(c), 1)))
    if t.shape[0] != c.shape[0]:
        raise ValueError('t and c dim. mismatch')
    instance.t = t
    instance.c = c
    instance.order = c.shape[1] / 2 - 1
    return instance



cdef class PiecewisePolynomial:
    """
    PiecewisePolynomial class (mimics scipy.interpolate.PiecewisePolynomial)
    """
    cdef public np.ndarray t
    cdef public np.ndarray c
    cdef public int order

    def __init__(self,
                 np.ndarray[np.float64_t, ndim=1] t,
                 np.ndarray[np.float64_t, ndim=2] y):
        cdef np.ndarray[np.float64_t, ndim=2] c_view = np.ascontiguousarray(np.empty(
            (y.shape[0], y.shape[1] * 2), dtype = np.float64))
        cdef np.ndarray[np.float64_t, ndim=2] y_view = np.ascontiguousarray(
            y, dtype=np.float64)

        self.order = y.shape[1] - 1
        if self.order == 0:
            poly_coeff1(<double*>t.data, <double*>y_view.data, <double*>c_view.data, len(t))
        elif self.order == 1:
            poly_coeff3(<double*>t.data, <double*>y_view.data, <double*>c_view.data, len(t))
        elif self.order == 2:
            poly_coeff5(<double*>t.data, <double*>y_view.data, <double*>c_view.data, len(t))

        self.t = np.ascontiguousarray(t.copy())
        self.c = np.ascontiguousarray(c_view.copy())

    def __call__(self, t):
        # These 3 are used in case of t is float
        cdef double y
        cdef size_t it
        cdef int j
        if not isinstance(t, np.ndarray):
            if isinstance(t, float):
                y = 0.0
                if self.t[0] <= t and t <= self.t[-1]:
                    it = get_interval(<double*>self.t.data, len(self.t), t)
                else:
                    raise ValueError('Out of bounds')
                for j in range((self.order + 1)*2):
                    y += (t - self.t[it]) ** j * self.c[it, j]
                return np.array(y, dtype = np.float64)
            t = np.array(t, dtype=np.float64)
        yout = np.ascontiguousarray(np.empty(t.shape, dtype = np.float64))
        self._interpol(np.ascontiguousarray(t), yout)
        return yout

    cdef _interpol(self,
                   np.ndarray[np.float64_t, ndim=1] t,
                   np.ndarray[np.float64_t, ndim=1] yout):
        """
        Modify `yout` inplace to store interpolated values at `t`
        """
        cdef size_t i = 0
        cdef size_t it
        cdef size_t j
        cdef size_t t_size = len(t)
        cdef double y

        if self.t[0] <= t[0] and t[-1] <= self.t[-1]:
            it  = get_interval(<double*>self.t.data, len(self.t), t[0])
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
        return PiecewisePolynomial_from_coefficients, (self.t, self.c)

