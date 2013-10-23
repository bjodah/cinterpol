# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Custom setup script for cInterpol to generate sources and
compile and link a mix of C and Fortran 2003 sources wrapped
using Cython.

The setup requires pycompilation (www.github.com/bjodah/pycompilation)
"""

# Python standard libaray imports
import os
import logging
import shutil
import tempfile
from distutils.core import setup
from distutils.command import build_ext

from pycompilation import pyx2obj, compile_sources, compile_py_so, fort2obj, get_mixed_fort_c_linker
from pycompilation.util import render_mako_template_to, get_abspath


cInterpol_dir = './cInterpol/'

DEBUG=False # Production?


def render_poly_coeff(tempd, maxord=5):
    from cInterpol.poly_coeff_expr import coeff_expr
    tmpl_path = './cInterpol/poly_coeffX_template.c'
    tgts = []
    for i in range(1,maxord+1,2):
        tgts.append(os.path.join(tempd, 'poly_coeff{}.c'.format(i)))
        subsd = coeff_expr(i)
        render_mako_template_to(tmpl_path, tgts[-1], subsd)
    return tgts


def run_compilation(tempd, logger=None):
    # Let's compile elemwise.c and wrap it using cython
    # source in elemwise_wrapper.pyx

    poly_coeff_sources = render_poly_coeff(tempd)

    for fname in ['core.so']:
        fullpath = os.path.join(cInterpol_dir, fname)
        if os.path.exists(fullpath):
            os.unlink(fullpath)

    for fname in ['core.pyx', 'fornberg.f90', 'newton_interval.c',
                  'newton_interval.h', 'poly_eval.c', 'poly_eval.h']:
        shutil.copy(os.path.join(cInterpol_dir, fname), tempd)

    poly_coeff_objs = compile_sources(
        poly_coeff_sources+['newton_interval.c']+['poly_eval.c'],
        options=['warn', 'pic', 'fast', 'c99', 'openmp'],
        cwd=tempd, logger=logger, run_linker=False)

    fornberg_obj = fort2obj('fornberg.f90', cwd=tempd,
                            extra_options=['fast'], logger=logger)

    core_obj = pyx2obj('core.pyx', cwd=tempd, logger=logger,
                       include_numpy=True, gdb=True, flags=['-g'])

    CmplrRnnr, extra_kwargs, preferred_vendor = get_mixed_fort_c_linker(metadir=tempd)
    so_path = compile_py_so(poly_coeff_objs+[fornberg_obj]+[core_obj],
                            CmplrRnnr, #FortranCompilerRunner,
                            cwd=tempd, logger=logger, options=['openmp'])
    return get_abspath(so_path, cwd=tempd)


class my_build_ext(build_ext.build_ext):
    def run(self):
        # honor the --dry-run flag
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        if not self.dry_run:
            tempd = tempfile.mkdtemp()
            try:
                so_path = run_compilation(tempd, logger=logger)
                shutil.copy(so_path, cInterpol_dir)
            finally:
                if not DEBUG:
                    shutil.rmtree(tempd)
        else:
            logger.info('did nothing.')


cmdclass = {'build_ext': my_build_ext}


from distutils.extension import Extension
ext_modules = [
    Extension('cInterpol.core', ['cInterpol/core.c']),
]


setup(
    name='cInterpol',
    cmdclass = cmdclass,
    ext_modules=[],#ext_modules,
    packages = ['cInterpol']
)
