# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Custom setup script for cInterpol to generate sources and
compile and link a mix of C and Fortran 2003 sources wrapped
using Cython. The complexity of this motivated use of `pycompilation`
an external library which abstracts away parts of this process.
"""

# Python standard libaray imports
import os
import logging
import shutil
import tempfile
from distutils.core import setup
from distutils.command import build_ext

# External imports
from pycompilation import (
    pyx2obj, compile_sources, compile_py_so, fort2obj,
    get_mixed_fort_c_linker)
from pycompilation.util import render_mako_template_to, get_abspath

# Intra project imports
from cInterpol.codeexport import ModelCode


cInterpol_dir = './cInterpol/'
DEBUG=True # Production?

model_tokens = ['poly'] #, 'pade'] #, 'lincomb'


def run_compilation(tokens, tempdir, max_wy, max_derivative,
                    logger=None):
    # Let's compile elemwise.c and wrap it using cython
    # source in elemwise_wrapper.pyx

    source_files = []
    for token in tokens:
        model_code = ModelCode(token, max_wy, max_derivative,
                               tempdir=tempdir)
        model_code.write_code()
        print(model_code._written_files)
        source_files.extend(model_code.source_files)

    for fname in ['core.so']:
        fullpath = os.path.join(cInterpol_dir, fname)
        if os.path.exists(fullpath):
            os.unlink(fullpath)

    render_mako_template_to(
        'cInterpol/piecewise_template.pyx',
        os.path.join(tempdir,'piecewise.pyx'),
        subsd={'tokens': tokens,
               'max_wy': max_wy,
               'max_derivative': max_derivative}
    )

    for fname in ['fornberg_wrapper.pyx', 'fornberg.f90',
                  'newton_interval.c', 'newton_interval.h']:
        shutil.copy(os.path.join(cInterpol_dir, fname), tempdir)

    token_coeff_objs = compile_sources(
        source_files+['newton_interval.c'],
        options=['warn', 'pic', 'fast', 'c99', 'openmp'],
        cwd=tempdir, logger=logger, run_linker=False)

    fornberg_objs = [
        fort2obj('fornberg.f90', cwd=tempdir,
                 extra_options=['fast'], logger=logger),
        pyx2obj('fornberg_wrapper.pyx', cwd=tempdir,
                logger=logger, include_numpy=True,
                gdb=True if DEBUG else False,
                flags=['-g'] if DEBUG else None),
    ]


    cy_objs = []
    for f in ['piecewise.pyx', 'fornberg_wrapper.pyx']:
        cy_objs.append(pyx2obj(f, cwd=tempdir, logger=logger,
                           include_numpy=True,
                           gdb=True if DEBUG else False,
                           flags=['-g'] if DEBUG else None))


    CmplrRnnr, extra_kwargs, preferred_vendor = \
        get_mixed_fort_c_linker(metadir=tempdir)
    so_path = compile_py_so(
        token_coeff_objs+fornberg_objs+cy_objs,
        CmplrRnnr, cwd=tempdir, logger=logger, options=['openmp'])

    return get_abspath(so_path, cwd=tempdir)


class my_build_ext(build_ext.build_ext):
    def run(self):
        # honor the --dry-run flag
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        if not self.dry_run:
            tempdir = tempfile.mkdtemp()
            try:
                print(model_tokens)
                so_path = run_compilation(
                    model_tokens,
                    tempdir, max_wy=3, max_derivative=3,
                    logger=logger)
                print(type(so_path))
                shutil.copy(so_path, cInterpol_dir)
            finally:
                if not DEBUG:
                    shutil.rmtree(tempdir)
        else:
            logger.info('did nothing.')


cmdclass = {'build_ext': my_build_ext}

setup(
    name='cInterpol',
    cmdclass = cmdclass,
    ext_modules=[],
    packages = ['cInterpol']
)
