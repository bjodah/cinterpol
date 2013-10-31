# -*- coding: utf-8 -*-

# stdlib imports
import sympy
import re

# external imports
from pycompilation.util import render_mako_template_to

# project internal imports
from cInterpol.model import models
from cInterpol.codeexport import C_Code

SIZE_T = 'int'

class ModelCode(C_Code):


    source_files = ['./cInterpol/coeff.c',
                    './cInterpol/eval.c']

    _templates = ['./cInterpol/coeff_template.c',
                  './cInterpol/coeff_template.h',
                  './cInterpol/eval_template.c',
                  './cInterpol/eval_template.h',]

    def __init__(self, token, max_wy, max_derivative, *args, **kwargs):
        self.max_wy = max_wy
        self.max_derivative = max_derivative
        self.Model = models[token]
        super(ModelCode, self).__init__(*args, **kwargs)


    def variables_for_wy(self, wy):


    def variables(self):
        # number of cofficients per peicewise segment
        wc = self.wy*2

        # Sympy variable symbols for formulating code
        xend = sympy.symbols('xend')
        ystart = [sympy.Symbol('ystart_' + str(i)) for i in range(wy)]
        yend = [sympy.Symbol('yend_' + str(i)) for i in range(wy)]

        m = self.Model(self.wy)
        eqs = []
        for i in range(wy):
            # x=0
            eqs.append(m.diff(i).subs({m.x: 0}) - ystart[i])
            # x=xend
            eqs.append(m.diff(i).subs({m.x: xend}) - yend[i])
        sol = sympy.solve(eqs, *m.c)

        cse_defs, code_block = self.get_cse_code(
            self._neqsys.exprs, 'cse', dummy_groups)

        # End block
        eqs = []
        for i in range(wy):
            # x=0
            eqs.append(m.diff(i).subs({m.x: xstart}) - ystart[i])
            # x=xend
            eqs.append(m.diff(i).subs({m.x: 0}) - yend[i])

        m_end = models[token](wy)
        sol = sympy.solve(eqs, *m.c)
        end_block = []
        for i, ci in enumerate(m.c):
            code = sympy.ccode(sol[ci])
            code = as_c_arr_expr_back(code)
            c_var = as_c_arr_expr_back(str(ci))
            end_block.append('{} = {};'.format(c_var, code))

        return {'cse_def': cse_def,
                'cse_block': cse_block,
                'main_block': main_block,
                'end_block': end_block,
                'cse_defs': cse_defs,
                'wy': wy,
                'SIZE_T': SIZE_T}


def render_coeff(token, tempdir, max_wy=3):
    tgts = []
    for i in range(1,max_wy+1):
        model_code = ModelCode(token, i, tempdirir=tempdirir)
        model_code.write_code()
        token_code._templates = ['./cInterpol/'+token+\
                                 '_coeffX_template.c']
        tgts.append(os.path.join(tempdir, token+'_coeff{}.c'.format(i)))
        subsd = template_expr(i)
        render_mako_template_to(tmpl_path, tgts[-1], subsd)
    return tgts, []
