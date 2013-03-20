#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sympy
import re

class Polynomial(object):

    x = sympy.Symbol('x', real = True)

    @property
    def c(self):
        return [sympy.Symbol('c_' + str(o), real = True) for o in range(self.order + 1)]


    def __init__(self, order):
        self.order = order

    def diff(self, deg):
        return self.expr.diff(self.x, deg)

    @property
    def expr(self):
        return sum([self.c[o]*self.x**o for o in range(self.order + 1)])



def coeff_expr(order):
    """
    Generate coeff fit expressions for order
    """
    assert order % 2 == 1
    wy = (order + 1)/ 2
    xend = sympy.symbols('xend')
    y0 = [sympy.Symbol('y0_' + str(i)) for i in range(wy)] # der order
    yend = [sympy.Symbol('yend_' + str(i)) for i in range(wy)] # der order
    p = Polynomial(order)
    eqs = []
    for i in range(wy):
        # x=0
        eqs.append(p.diff(i).subs({p.x: 0}) - y0[i])
        # x=xend
        eqs.append(p.diff(i).subs({p.x: xend}) - yend[i])

    sol = sympy.solve(eqs, *p.c)

    wc = (order + 1)
    wy = (order + 1) / 2
    block = []
    for i, ci in enumerate(p.c):
        code = sympy.ccode(sol[ci])
        code = code.replace(str(xend), 'dt')
        code = re.sub(r'y0_(\d+)', r'y[i*{}+\1]'.format(wy), code)
        code = re.sub(r'yend_(\d+)', r'y[(i+1)*{}+\1]'.format(wy), code)
        c_var = re.sub(r'c_(\d+)', r'c[i*{}+\1]'.format(wc), str(ci))
        block.append('{} = {};'.format(c_var, code))

    endblock = []
    for i, ci in enumerate(p.c):
        if i < (order + 1) / 2:
            code = 'y[i*{}+{}]'.format(wy, i)
        else:
            code = '0'
        c_var = re.sub(r'c_(\d+)', r'c[i*{}+\1]'.format(wc), str(p.c[i]))
        endblock.append('{} = {};'.format(c_var, code))

    return {'main_block': block, 'end_block': endblock,
            'ORDER': order}

if __name__ == '__main__':
    blocks = coeff_expr(1)
    print '\n'.join(blocks['main_block'])
    print ''
    print '\n'.join(blocks['end_block'])

