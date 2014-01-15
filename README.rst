=============
cInterpol
=============

cInterpol_ is a python extension for optimized interpolation of
data series for which each data point one knows the up to N-th order derivative.

It provides a close to 6 orders of magnitude faster (albeit less general)
version of `scipy.interpolate.PiecewisePolynomial` (my Core i7-3770K give ~800 000x speed-up). 

See examples/perf.py for a quick head-on benchmark between those two
(expect a runtime on the order of half a minute).  The performance is
achieved through the use of multithreaded (OpenMP) C routines (wrapped using Cython).

The formulae for the coefficients are generated using Sympy, and can in theory be modified quite easily.

Feel free to enhance modify and make pull request at `github`__ to

.. _cInterpol: http://www.github.com/bjodah/cinterpol

__ cinterpol_


Installation
============
Using pip:
`pip install https://github.com/bjodah/cinterpol/archive/v0.2.2.tar.gz`
Manual installation:
1. Clone repository `git clone https://github.com/bjodah/cinterpol.git`
2. Install dependencies `cd cinterpol; pip install -r requirements.txt`
3. Install run `sudo python setup.py install` or `python setup.py install --user`.

See distutils' documentation_ for more options.
.. _documentation: http://docs.python.org/2/library/distutils.html

Tests
=====
Run `py.test` if py.test is installed on your system.
Elsewise: `cd cInterpol/tests/; make tests`

Performance tests
-----------------
See examples/perf.py, as of SciPy 0.11 you should expect about 5
orders of magnitude speed-up.


Dependencies
============
* Python_
* NumPy_
* Cython_ >= v0.19.1
* Sympy_ 
* pycompilation_ >= v0.2.2
.. _Python: http://www.python.org
.. _NumPy: http://www.numpy.org/
.. _Cython: http://www.cython.org/
.. _Sympy: http://sympy.org/
.. _pycompilation: https://www.github.com/bjodah/pycompilation

TODO
====
Add monotonic interpolator
Add cubic splines (+monotone)

Notes
=====
There is a git subtree under cInterpol, update though:
`git subtree --prefix cInterpol/newton_interval pull newton_interval master`
where the repo "newton_interval" is https://github.com/bjodah/newton_interval.git


License
=======
Open Soucrce. Released under the very permissive "simplified
(2-clause) BSD license". See LICENCE.txt for further details.

Author
======
Björn Dahlgren, contact (gmail adress): bjodah
