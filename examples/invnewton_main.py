#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import, unicode_literals

import logging

import argh
import matplotlib.pyplot as plt
import numpy as np
import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application


from cInterpol.invnewton import InvNewtonCode

try:
    from symvarsub.numtransform import lambdify
except IOError:
    from sympy.utilities.lambdify import lambdify


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__file__)


# y=x/(1+x) has the inverse x = y/(1-y), it is monotonic for x>-1 and x<-1 (inc/inc)
def main(yexprstr='x/(1+x)', lookup_N = 5, order=3, x_lo=0.0, x_hi=1.0,
         x='x', save_temp=True, sample_N=42, check_monotonicity=False,
         itermax=20):
    # Parse yexprstr
    yexpr = parse_expr(yexprstr, transformations=(
        standard_transformations + (implicit_multiplication_application,)))
    x = sympy.Symbol(x, real=True)
    yexpr = yexpr.subs({sympy.Symbol('x'): x})

    y = sympy.Symbol('y', real=True)
    explicit_inverse = sympy.solve(yexpr-y,x)
    if explicit_inverse:
        if len(explicit_inverse) == 1:
            print('Explicit inverse: ' + str(explicit_inverse))
            explicit_inverse = explicit_inverse[0]
        else:
            print('No explicit inverse')
            explicit_inverse = None

    # Generate code
    code = InvNewtonCode(
        yexpr, lookup_N, order, (x_lo, x_hi), x, check_monotonicity,
        save_temp=save_temp, tempdir='build_invnewton', logger=logger)
    ylim = code.ylim
    mod = code.compile_and_import_binary()

    # Calculate inverse for some randomly sampled values of y on span
    yspan = ylim[1]-ylim[0]
    yarr = ylim[0]+np.random.random(sample_N)*yspan
    xarr = mod.invnewton(yarr, itermax=itermax)

    # Plot the results
    if explicit_inverse:
        plt.subplot(212)
        cb_expl = lambdify(y, explicit_inverse)
        xarr_expl = cb_expl(yarr).flatten()
        plt.plot(yarr, xarr_expl-xarr, 'x', label='Error')
        plt.ylabel('x')
        plt.xlabel('y')
        plt.legend()
        plt.subplot(211)
        plt.plot(yarr, xarr_expl, 'x', label='Analytic')

    plt.plot(yarr, xarr, 'o', label='Numerical')
    plt.ylabel('x')
    plt.xlabel('y')
    plt.legend()
    plt.show()

argh.dispatch_command(main)
