=============
cInterpol
=============

cInterpol_ is a small python extension for optimized interpolation of
data series for which each time point has up to N-th order derivative.

It provides a c:a 3 orders of magnitude faster (albeit less general)
version of `scipy.interpolate.PiecewisePolynomial`. The greatest speed
up requires passing check_nan=False to PiecewisePolynomial.__init__,
check_nan=True (default) make runtime twice (perf.py) as long (for
now).

See examples/perf.py for a quick head-on benchmark between those two
(expect a runtime on the order of one minute).  The performance is
achieved through the use of plain C (with some equations generated
through Sympy) and Cython.

Feel free to enhance modify and make pull request at `github`__ to

.. _cinterpol: http://www.github.com/bjodah/cinterpol

__ cinterpol_

Installation
============
To install run `python setup.py install`.
See distutils' documentation_ for more options.

.. _documentation: http://docs.python.org/2/library/distutils.html

Files
=====
core.pyx - The pythonic (cython) interface to the C routines
newton_interval.c - Quadratic order look up see 
poly_coeffX.c.mako
poly_coeff_expr.py

Tests
=====
TODO: make a proper test suite.
For now the examples serves as tests together with
the tests in symodesys/tests (read MANIFEST.txt therein)


Performance tests
-----------------
See examples/perf.py, as of SciPy 0.11 you should expect about 3
orders of magnitude speed-up.


Dependencies
============
Python_
NumPy_
Mako_   (optional)
Cython_ 0.19 (optional)
Sympy_  (optional)

.. _Python: http://www.python.org
.. _NumPy: http://www.numpy.org/
.. _Mako: http://www.makotemplates.org/
.. _Cython: http://www.cython.org/
.. _Sympy: http://sympy.org/

Bits and pieces with potential for usage outside cInterpol
==============================================================
newton_interval.c - Even though very simple it can be useful for quadratic
convergence lookup in ordered (strictly monotone) and well behaved arrays.

TODO
====
Add cubic splines
Add finite difference (Fornberg)

License
=======
Open Soucrce. Released under the very permissive "simplified
(2-clause) BSD license". See LICENCE.txt for further details.

Author
======
Björn Dahlgren, contact (gmail adress): bjodah
