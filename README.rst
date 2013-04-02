=============
cinterpol
=============

cinterpol is a small python package for optimized interpolation of data series for which
each time point has up to N-th order derivative.

It provides a faster (c:a 1000 X speed-up) version (and less general) of scipy.interpolate.PiecewisePolynomial

See examples/perf.py for a quick head-on benchmark between those two (beware of runtime of about ~1 min).

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
newton_interval.c - Even though very simple it can be useful (once tested thoroughly) for quadratic convergence lookup in ordered (and well behaved) arrays.

License
=======
Open Soucrce. Released under the very permissive "simplified (2-clause) BSD license". See LICENCE.tx for further details.


