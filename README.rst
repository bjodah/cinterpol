=============
cinterpol
=============

cinterpol is a small python extension for optimized interpolation of data series for which
each time point has up to N-th order derivative.

It provides a c:a 3 orders of magnitude faster (albeit less general) version of scipy.interpolate.PiecewisePolynomial

See examples/perf.py for a quick head-on benchmark between those two (expect a runtime on the order of one minute).
The performance is achieved through the use of plain C (with some equations generated through Sympy) and Cython.

Installation
============
To install run `python setup.py build_ext --inplace`

Files
=====
core.pyx
newton_interval.c
poly_coeffX.c.mako
poly_coeff_expr.py

Tests
=====

Unittests
---------
tests/test_core.py

Performance tests
-----------------
perf/


Dependencies
============
python
numpy
mako   (optional)
cython (optional)
sympy  (optional)

Bits and pieces with potential for usage outside Fast Interpol
==============================================================
newton_interval.c - Even though very simple it can be useful (once tested thoroughly) for quadratic convergence lookup in ordered (strictly monotone) and well behaved arrays.

License
=======
Open Soucrce. Released under the very permissive "simplified (2-clause) BSD license". See LICENCE.tx for further details.

