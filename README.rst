=============
cinterpol
=============

cinterpol is a small python package for optimized interpolation of data series for which
each time point has up to N-th order derivative.

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
mako   (for building)
cython (for building)
sympy  (for building)

Bits and pieces with potential for usage outside Fast Interpol
==============================================================
newton_interval.c - Even though very simple it can be useful (once tested thoroughly) for quadratic convergence lookup in ordered (and well behaved) arrays.

License
=======
Open Soucrce. Released under the very permissive simplified (2-clause) BSD license. See LICENCE.tx for f
urther details.


