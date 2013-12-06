#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Custom setup script for cInterpol to generate sources and
compile and link a mix of C and Fortran 2003 sources wrapped
using Cython.

The setup requires pycompilation (www.github.com/bjodah/pycompilation)
"""

# Python standard libaray imports
import os
import logging
import tempfile
import shutil
from distutils.core import setup
from distutils.command import build_ext

from pycompilation import pyx2obj, compile_sources, compile_py_so, src2obj, get_mixed_fort_c_linker
from pycompilation.util import render_mako_template_to, get_abspath, copy, MetaReaderWriter


cInterpol_dir = './cInterpol/'

if os.path.exists('./.git'):
    # Production?
    DEBUG=True
else:
    DEBUG=False


def render_poly_coeff(tempd, maxord=5):
    from cInterpol.poly_coeff_expr import coeff_expr
    tmpl_path = './cInterpol/poly_coeffX_template.c'
    tgts = []
    for i in range(1,maxord+1,2):
        tgts.append(os.path.join(tempd, 'poly_coeff{}.c'.format(i)))
        subsd = coeff_expr(i)

        metakey = 'poly_coeff_subsd_'+str(i)
        meta = MetaReaderWriter('.meta_poly_coeff')
        try:
            prev_subsd = meta.get_from_metadata_file(
                cInterpol_dir, metakey)
        except (IOError, KeyError):
            prev_subsd = None
        outpath = render_mako_template_to(tmpl_path, tgts[-1], subsd,
                                only_update=True, prev_subsd=prev_subsd)
        if outpath:
            meta.save_to_metadata_file(cInterpol_dir, metakey, subsd)
    return tgts


def run_compilation(tempd, **kwargs):
    # Let's compile elemwise.c and wrap it using cython
    # source in elemwise_wrapper.pyx

    poly_coeff_sources = render_poly_coeff(tempd)

    for fname in ['core.so']:
        fullpath = os.path.join(cInterpol_dir, fname)
        if os.path.exists(fullpath):
            os.unlink(fullpath)

    for fname in ['core.pyx', 'fornberg.f90', 'newton_interval.c',
                  'newton_interval.h', 'poly_eval.c', 'poly_eval.h']:
        copy(os.path.join(cInterpol_dir, fname), tempd,
             only_update=kwargs.get('only_update', False))

    poly_coeff_objs = compile_sources(
        poly_coeff_sources+['newton_interval.c']+['poly_eval.c'],
        options=['warn', 'pic', 'openmp'],
        std='c99',
        cwd=tempd, run_linker=False, **kwargs)

    fornberg_obj = src2obj(
        'fornberg.f90',
        options=['warn', 'pic', 'fast',  'openmp'],
        cwd=tempd, **kwargs)

    core_obj = pyx2obj('core.pyx', cwd=tempd,
                       include_numpy=True, gdb=True,
                       options=['warn', 'fast'],
                       flags=['-g'], **kwargs)

    CmplrRnnr, extra_kwargs, preferred_vendor = get_mixed_fort_c_linker(metadir=tempd)
    so_path = compile_py_so(poly_coeff_objs+[fornberg_obj]+[core_obj],
                            CmplrRnnr, cwd=tempd, options=['warn', 'pic', 'fast', 'openmp'], **kwargs)
    return get_abspath(so_path, cwd=tempd)


class my_build_ext(build_ext.build_ext):
    def run(self):
        # honor the --dry-run flag
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        if not self.dry_run:
            tempd = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'build')
            if not os.path.exists(tempd): os.mkdir(tempd)
            #tempd = tempfile.mkdtemp()
            try:
                so_path = run_compilation(tempd, logger=logger, only_update=True)
                copy(so_path, cInterpol_dir)
                prebuild_invnewton_wrapper(
                    'prebuilt/', cwd=cInterpol_dir, logger=logger)

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
