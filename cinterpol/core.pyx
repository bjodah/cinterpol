import numpy as np
cimport numpy as np

cdef extern size_t get_interval(double arr[], size_t N, double t)
cdef extern size_t poly_coeff1(double t[], double y[], double c[], size_t nt)
cdef extern size_t poly_coeff3(double t[], double y[], double c[], size_t nt)
cdef extern size_t poly_coeff5(double t[], double y[], double c[], size_t nt)

cdef class PieceWisePolyInterpol:
    """
    PieceWisePolyInterpol class
    """
    cdef double [:] t
    cdef double [:,:] c
    cdef int order

    def __cinit__(self, t, c):
        if isinstance(t, np.ndarray):
            assert t.flags.aligned      # get_interval assumes aligned
            assert t.flags.c_contiguous # get_interval assumes c-contiguous
        else:
            t = np.ascontiguousarray(t)

        if isinstance(c, np.ndarray):
            assert c.flags.aligned      # poly_coeffX assumes aligned
            assert c.flags.c_contiguous # poly_coeffX assumes c-contiguous
        else:
            c = np.ascontiguousarray(c)

        if c.ndim == 1:
            c = np.ascontiguousarray(c.reshape((len(c), 1)))
        assert t.shape[0] == c.shape[0]
        self.t = t
        self.c = c
        self.order = c.shape[1] - 1
        cdef size_t i, j

    @classmethod
    def mk_from_array(self, double [:] t, double [:,:] y):
        c = np.ascontiguousarray(np.zeros(
            (y.shape[0], y.shape[1] * 2), dtype = np.float64))
        cdef double [:,:] c_view = c
        if y.shape[1] == 1:
            poly_coeff1(&t[0], &y[0, 0], &c_view[0, 0], len(t))
        elif y.shape[1] == 2:
            poly_coeff3(&t[0], &y[0, 0], &c_view[0, 0], len(t))
        elif y.shape[1] == 3:
            poly_coeff5(&t[0], &y[0, 0], &c_view[0, 0], len(t))
        return PieceWisePolyInterpol(t, c)

    def __call__(self, t):
        # These 3 are used in case of t is float
        cdef double y
        cdef size_t it
        cdef int j
        if not isinstance(t, np.ndarray):
            if isinstance(t, float):
                y = 0.0
                if self.t[0] <= t and t <= self.t[-1]:
                    it = get_interval(&self.t[0], len(self.t), t)
                else:
                    raise ValueError('Out of bounds')
                for j in range(self.order + 1):
                    y += (t - self.t[it]) ** j * self.c[it, j]
                return y
            t = np.array(t)
        yout = np.ascontiguousarray(np.zeros(t.shape, dtype = np.float64))
        self.interpol(t, yout)
        return yout

    def interpol(self, double [:] t, double [:] yout):
        """
        Modify `yout` inplace to store interpolated values at `t`
        """
        cdef size_t i = 0
        cdef size_t it
        cdef size_t j
        cdef size_t t_size = len(t)
        cdef double y = 0.0

        if self.t[0] <= t[0] and t[0] <= self.t[-1]:
            it  = get_interval(&self.t[0], len(self.t), t[0])
        else:
            raise ValueError('Out of bounds')

        while i < t_size:
            if t[i] > self.t[it + 1]:
                it += 1
                continue
            y = 0.0
            for j in range(self.order + 1):
                y += (t[i] - self.t[it]) ** j * self.c[it, j]
            yout[i] = y
            i += 1

    def __reduce__(self):

        fused = np.empty((self.c.shape[0], self.c.shape[1] + 1), dtype = np.float64)
        fused[:, 0] = self.t
        fused[:, 1:] = self.c
        return PieceWisePolyInterpol, (), fused

    def __setstate__(self, fused):
        self.t = fused[:, 0]
        self.c = fused[:, 1:]

    # Diagnostics
    def get_c(self):
        return np.array(self.c)

    def get_t(self):
        return np.array(self.t)

