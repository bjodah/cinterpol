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

name_ = 'cInterpol'
version_ = '0.2.1'

pkg_dir = name_
newton_interval_dir = os.path.join(name_, 'newton_interval')
model_tokens = ['poly'] #, 'pade'] #, 'lincomb'


if '--help'in sys.argv[1:] or sys.argv[1] in (
        '--help-commands', 'egg_info', 'clean', '--version'):
    cmdclass_ = {}
    ext_modules_ = []
else:
    from pycompilation.dist import clever_build_ext
    from pycompilation.dist import CleverExtension as Extension
    from .cInterpol.model import models
    from .cInterpol.codeexport import ModelCode
    source_files = [
        os.path.join(newton_interval_dir, 'src', 'newton_interval.c'),
        os.path.join(pkg_dir, 'piecewise_template.pyx'),
    ],

    for token in model_tokens:
        model_code = ModelCode(
            models[token], max_wy, max_derivative,
            tempdir=pkg_dir)
        model_code.write_code()
        print(model_code._written_files) ## DEBUG
        source_files.extend(model_code.source_files)

    subsd =  {'tokens': model_tokens,
              'max_wy': max_wy,
              'max_derivative': max_derivative}

    subsd.update(code.variables)

    cmdclass_ = {'build_ext': clever_build_ext},
    ext_modules_ = [
        CleverExtension(
            name_+".piecewise",
            sources=source_files
            include_dirs=[os.path.join(newton_interval_dir, 'include')],
            template_regexps=[
                (r'^(\w+)_template.(\w+)$', r'\1.\2', subsd),
            ],
            options_per_file={
                'eval.c': ['pic', 'warn', 'fast', 'openmp'],
                'coeff.c': ['pic', 'warn', 'fast', 'openmp'],
                }
        )
    ]


setup(
    name=name_,
    version=version_,
    author='Björn Dahlgren',
    author_email='bjodah@DELETEMEgmail.com',
    description="Python extension for optimized interpolation of "+\
    "data series for which each data point has up to N-th order derivative.",
    license = "BSD",
    url='https://github.com/bjodah/'+name_.lower(),
    download_url='https://github.com/bjodah/'+name_.lower()+'/archive/v'+version_+'.tar.gz',
    packages = [name_]
    ext_modules=ext_modules_,
    cmdclass = cmdclass_,
)


    # poly_coeff_objs = compile_sources(
    #     poly_coeff_sources+['newton_interval.c']+['poly_eval.c'],
    #     options=['warn', 'pic', 'fast', 'openmp'],
    #     std='c99',
    #     cwd=tempd, run_linker=False, **kwargs)

    # core_obj = pyx2obj('core.pyx', cwd=tempd,
    #                    include_numpy=True, gdb=True,
    #                    options=['warn', 'fast'],
    #                    flags=['-g'], **kwargs)

    # so_path = link_py_so(
    #     poly_coeff_objs+[core_obj], cwd=tempd,
    #     options=['warn', 'pic', 'fast', 'openmp'], **kwargs)
