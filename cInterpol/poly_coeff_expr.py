#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sympy
import re

from cInterpol.util import Polynomial

# TODO: use pycompilation for render_mako_template_to
from mako.template import Template
def render_mako_template_to(template_path, outpath, subsd):
    template_str = open(template_path, 'rt').read()
    ofh = open(outpath, 'wt')
    ofh.write(Template(template_str).render(**subsd))
    ofh.close()


def poly_expr(wy):
    """
    Generate coeff fit expressions for order
    """
    # assert order % 2 == 1
    wy = (order + 1)/ 2
    wc = (order + 1)
    xend = sympy.symbols('xend')
    ystart = [sympy.Symbol('ystart_' + str(i)) for i in range(wy)]
    yend = [sympy.Symbol('yend_' + str(i)) for i in range(wy)]

    def as_c_arr_expr(ccode):
        ccode = ccode.replace(str(xend), 'dt')
        ccode = re.sub(r'ystart_(\d+)', r'y[i*{}+\1]'.format(wy),
                       ccode)
        ccode = re.sub(r'yend_(\d+)', r'y[(i+1)*{}+\1]'.format(wy),
                       ccode)
        ccode = re.sub(r'c_(\d+)', r'c[i*{}+\1]'.format(wc),
                       ccode)
        return ccode


    p = Polynomial(order)
    eqs = []
    for i in range(wy):
        # x=0
        eqs.append(p.diff(i).subs({p.x: 0}) - ystart[i])
        # x=xend
        eqs.append(p.diff(i).subs({p.x: xend}) - yend[i])

    sol = sympy.solve(eqs, *p.c)
    cse_defs, cse_exprs = sympy.cse(sol.values())
    modsol = dict(zip(sol.keys(), cse_exprs))

    cseblock = []
    csedef = []
    for var_name, var_expr in cse_defs:
        c_var_expr = as_c_arr_expr(sympy.ccode(var_expr))
        csedef.append('double {};'.format(var_name))
        cseblock.append('{} = {};'.format(var_name, c_var_expr))


    block = []
    for i, ci in enumerate(p.c):
        code = sympy.ccode(modsol[ci])
        code = as_c_arr_expr(code)
        c_var = as_c_arr_expr(str(ci))
        block.append('{} = {};'.format(c_var, code))

    return {'cse_def': csedef, 'cse_block': cseblock,
            'main_block': block, 'end_block': _get_end_block(order),
            'cse_defs': cse_defs,
            'ORDER': order}

def _get_end_block(order):
    """
    Solve with back diff for last cell.
    """
    assert order % 2 == 1
    wy = (order + 1)/ 2
    wc = (order + 1)
    xend = sympy.symbols('xend')
    ystart = [sympy.Symbol('ystart_' + str(i)) for i in range(wy)]
    yend = [sympy.Symbol('yend_' + str(i)) for i in range(wy)]

    # For last point we use back-diff
    xstart = sympy.symbols('xstart')
    def as_c_arr_expr_back(ccode):
        ccode = ccode.replace(str(xstart), '-dt')
        ccode = re.sub(r'ystart_(\d+)', r'y[(i-1)*{}+\1]'.format(wy),
                       ccode)
        ccode = re.sub(r'yend_(\d+)', r'y[i*{}+\1]'.format(wy),
                       ccode)
        ccode = re.sub(r'c_(\d+)', r'c[i*{}+\1]'.format(wc),
                       ccode)
        return ccode

    p = Polynomial(order)
    eqs = []
    for i in range(wy):
        # x=0
        eqs.append(p.diff(i).subs({p.x: xstart}) - ystart[i])
        # x=xend
        eqs.append(p.diff(i).subs({p.x: 0}) - yend[i])

    sol = sympy.solve(eqs, *p.c)


    block = []
    for i, ci in enumerate(p.c):
        code = sympy.ccode(sol[ci])
        code = as_c_arr_expr_back(code)
        c_var = as_c_arr_expr_back(str(ci))
        block.append('{} = {};'.format(c_var, code))

    return block


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print('hit')
        blocks = coeff_expr(int(sys.argv[1]))
    else:
        blocks = coeff_expr(1)
    print '\n'.join(blocks['cse_def'])
    print ''
    print '\n'.join(blocks['cse_block'])
    print ''
    print '\n'.join(blocks['main_block'])
    print ''
    print '\n'.join(blocks['end_block'])
