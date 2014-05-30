#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Custom setup script for cInterpol to generate sources and
compile and link a C routines (and their Cython wrappers).

The setup requires pycompilation (www.github.com/bjodah/pycompilation)
"""

# Python standard libaray imports
import os
import sys
from distutils.core import setup

name_ = 'cInterpol'
version_ = '0.3.3'


pkg_dir = name_
newton_interval_dir = os.path.join(name_, 'newton_interval')

# What code to generate...
max_wy = 3
model_tokens = ['poly'] #, 'pade'] #, 'lincomb'

if '--help'in sys.argv[1:] or sys.argv[1] in (
        '--help-commands', 'egg_info', 'clean', '--version'):
    cmdclass_ = {}
    ext_modules_ = []
else:
    import numpy
    from pycompilation.dist import clever_build_ext
    from pycompilation.dist import CleverExtension
    from cInterpol.model import models
    from cInterpol.codeexport import ModelCode
    newton_interval_c_src = os.path.join(newton_interval_dir, 'src', 'newton_interval.c')
    source_files = [
        os.path.join(pkg_dir, 'piecewise_template.pyx'),
        newton_interval_c_src,
    ]

    for token in model_tokens:
        model_code = ModelCode(
            model_tokens, [models[tok] for tok in model_tokens],
            max_wy, tempdir=pkg_dir)
        model_code.write_code()
        print(model_code._written_files) ## DEBUG
        source_files = model_code.source_files + source_files

    subsd =  {'tokens': model_tokens,
              'max_wy': max_wy,
    }

    subsd.update(model_code.variables())

    cmdclass_ = {'build_ext': clever_build_ext}
    ext_modules_ = [
        CleverExtension(
            name_+".piecewise",
            sources=source_files,
            include_dirs=['./cInterpol', os.path.join(newton_interval_dir, 'include'), numpy.get_include()],
            template_regexps=[
                (r'^(\w+)_template.(\w+)$', r'\1.\2', subsd),
            ],
            pycompilation_compile_kwargs={
                'per_file_kwargs': {
                    newton_interval_c_src: {'std': 'c99'},
                    './cInterpol/eval.c': {
                        'std': 'c99',
                        'options': ['pic', 'warn', 'fast', 'openmp']
                    },
                    './cInterpol/coeff.c': {
                        'std': 'c99',
                        'options': ['pic', 'warn', 'fast', 'openmp']
                    },
                },
            },
            pycompilation_link_kwargs={
                'options': ['openmp'],
                #'libs': ['m']
            },
            logger=True,
        )
    ]

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: C",
    "Programming Language :: Cython",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
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
    packages = [name_],
    ext_modules=ext_modules_,
    cmdclass = cmdclass_,
)
