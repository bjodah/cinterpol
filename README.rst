=============
cInterpol
=============
.. image:: https://travis-ci.org/bjodah/cinterpol.png?branch=master
   :target: https://travis-ci.org/bjodah/cinterpol

cInterpol_ is a python extension for optimized interpolation of
data series where one for each data point knows a fixed number of derivatives 
(currently supported number of derivates are 0, 1, 2).

It provides a close to 6 orders of magnitude faster (albeit less general)
version of ``scipy.interpolate.PiecewisePolynomial`` (my Core i7-3770K give ~800 000x speed-up). 

See examples/perf.py for a quick head-on benchmark between those two
(expect a runtime on the order of half a minute).  The performance is
achieved through the use of multithreaded (OpenMP) C routines (wrapped using Cython).

The formulae for the coefficients are generated using Sympy, and can in 
theory be modified quite easily. (relevant files: model.py, codeexport.py, \*_template.\*)

Feel free to enhance modify and make pull request at `github`__.

.. _cInterpol: http://www.github.com/bjodah/cinterpol

__ cinterpol_


Installation
============
Example using pip (modify to your own needs):

    1. ``pip install --user --upgrade -r https://raw.github.com/bjodah/cinterpol/master/requirements.txt``
    2. ``pip install --user --upgrade https://github.com/bjodah/cinterpol/archive/v0.3.3.tar.gz``

Manual installation:
    1. Clone repository ``git clone https://github.com/bjodah/cinterpol.git``
    2. Install dependencies ``cd cinterpol; pip install --user --upgrade -r requirements.txt``
    3. To install run ``python setup.py install --user`` or ``sudo python setup.py install``.

See distutils' documentation_ for more options.
.. _documentation: http://docs.python.org/2/library/distutils.html

Note that the behaviour of ``setup(...)`` is modified slightly through the use of "CleverExtension" from pycompilation.

Tests
=====
Run ``py.test`` if py.test is installed on your system.
Elsewise: ``cd cInterpol/tests/; make``

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
* pycompilation_ >= v0.2.9
.. _Python: http://www.python.org
.. _NumPy: http://www.numpy.org/
.. _Cython: http://www.cython.org/
.. _Sympy: http://sympy.org/
.. _pycompilation: https://www.github.com/bjodah/pycompilation

TODO
====
Some templates unnecessarily rerendered during setup.
Add monotonic interpolator
Add cubic splines (+monotone)

Notes
=====
There is a git subtree under cInterpol, update through:
`git subtree --prefix cInterpol/newton_interval pull newton_interval master`
where the repo "newton_interval" is https://github.com/bjodah/newton_interval.git


License
=======
Open Soucrce. Released under the very permissive "simplified
(2-clause) BSD license". See LICENSE.txt for further details.

Author
======
Björn Dahlgren, contact (gmail adress): bjodah
