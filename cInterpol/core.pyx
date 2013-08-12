import numpy as np
cimport numpy as cnp
from cpython cimport bool


cdef extern size_t get_interval(const double arr[], const size_t N, const double t)
cdef extern void poly_coeff1(const double t[], const double y[], double c[], const size_t nt)
cdef extern void poly_coeff3(const double t[], const double y[], double c[], const size_t nt)
cdef extern void poly_coeff5(const double t[], const double y[], double c[], const size_t nt)
# Note above: Cython >=0.19 support const properly.

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


cdef ensure_contiguous(arr):
    if isinstance(arr, np.ndarray):
        if arr.flags.c_contiguous:
            return arr
        else:
            return np.ascontiguousarray(arr)
    else:
        return np.ascontiguousarray(arr)


cpdef PiecewisePolynomial PiecewisePolynomial_from_coefficients(t, c, allow_extrapol=True):
    t = ensure_contiguous(t)
    c = ensure_contiguous(c)
    return PiecewisePolynomial(t, c, c, allow_extrapol)


cdef class PiecewisePolynomial:
    """
    PiecewisePolynomial class (mimics scipy.interpolate.PiecewisePolynomial)
    """
    cdef public double [:] t
    cdef public double [:,:] c
    cdef public int order
    cdef public bool allow_extrapol


    def __cinit__(self, double [:] t, double [:,:] y, _c = None,
                  allow_extrapol=True, check_nan=True,
                  check_strict_monotonicity=True):
        """ Sets t, c and order"""
        cdef cnp.ndarray[cnp.float64_t, ndim=2] c = \
            np.ascontiguousarray(np.empty((y.shape[0], y.shape[1] * 2),
                                          dtype = np.float64))
        if _c != None:
            # init from t and c
            self.t = ensure_contiguous(t)
            self.c = ensure_contiguous(_c)
            self.order = _c.shape[1] - 1
            self.allow_extrapol = allow_extrapol
        else:
            # init from t and y
            t = ensure_contiguous(t)
            y = ensure_contiguous(y)

            self.allow_extrapol = allow_extrapol
            self.order = y.shape[1] * 2 - 1
            if self.order == 1:
                poly_coeff1(&t[0], &y[0,0], &c[0,0], len(t))
            elif self.order == 3:
                poly_coeff3(&t[0], &y[0,0], &c[0,0], len(t))
            elif self.order == 5:
                poly_coeff5(&t[0], &y[0,0], &c[0,0], len(t))

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


    cdef int _get_c_index(self, double t):
        if t < self.t[0]:
            if self.allow_extrapol == True:
                return 0
            else:
                raise ValueError(
                    'Out of bounds (allow_extrapol set to False)')
        elif t > self.t[-1]:
            if self.allow_extrapol == True:
                return len(self.t)-1
            else:
                raise ValueError(
                    'Out of bounds (allow_extrapol set to False)')
        else:
            return get_interval(&self.t[0], len(self.t), t)


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
                it = self._get_c_index(t)
                for j in range(self.order+1):
                    y += (t - self.t[it])**j * self.c[it, j]
                return np.array(y, dtype = np.float64)
            t = np.array(t, dtype=np.float64)

        yout = np.ascontiguousarray(np.empty(t.shape, dtype=np.float64))
        self._interpol(t, yout)
        return np.asarray(yout)


    def derivative(self, int nth=1):
        if nth == 0:
            return self
        if nth == 1:
            assert self.order >= 1
            new_c = self.c[:,1:]*np.arange(1, self.order+1).reshape(
                (1, self.order))
            return PiecewisePolynomial_from_coefficients(
                self.t, new_c, allow_extrapol=self.allow_extrapol)
        elif nth > 1:
            # recursive solution
            assert nth <= self.order
            return self.derivative(1).derivative(nth-1)
        else:
            raise ValueError("That would be the integral?")


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
        cdef size_t c_size = self.c.shape[0]
        cdef double y
        it = self._get_c_index(t[0])

        while i < t_size:
            if t[i] > self.t[it + 1]:
                if it < (c_size-2):
                    it += 1
                    continue
            y = 0.0
            for j in range(self.order+1):
                y += (t[i] - self.t[it]) ** j * self.c[it, j]
            yout[i] = y
            i += 1


    def __reduce__(self):
        return PiecewisePolynomial_from_coefficients, (
            np.asarray(self.t), np.asarray(self.c), self.allow_extrapol)

# Below is for wrapping finitediff.c

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


cdef get_weights(double [:] xarr, double xtgt, int n, int maxorder=0):
    cdef cnp.ndarray[cnp.float64_t, ndim=2, mode='fortran'] c = \
        np.zeros((n, maxorder+1), order='F')
    cdef int nm1 = n-1 # n minus 1
    populate_weights(&xtgt, &xarr[0], &nm1, &maxorder, &c[0,0])
    return c
