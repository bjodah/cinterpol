# -*- coding: utf-8 -*-

# stdlib imports
import sympy
import re
from collections import defaultdict

# external imports
from pycompilation.codeexport import C_Code
from pycompilation.util import render_mako_template_to

# project internal imports
from cInterpol.model import models


SIZE_T = 'int'

class ModelCode(C_Code):


    source_files = ['coeff.c',
                    'eval.c']

    templates = ['./cInterpol/coeff_template.c',
                  './cInterpol/coeff_template.h',
                  './cInterpol/eval_template.c',
                  './cInterpol/eval_template.h',]

    def __init__(self, token, max_wy, max_deriv, *args, **kwargs):
        self.max_wy = max_wy
        self.max_deriv = max_deriv
        self.Model = models[token]
        super(ModelCode, self).__init__(*args, **kwargs)


    def variables_for_wy(self, wy):
        # number of cofficients per peicewise segment
        wc = wy*2

        # Sympy variable symbols for formulating code
        y0 = [sympy.Symbol('y0_' + str(i)) for i in range(wy)]
        y1 = [sympy.Symbol('y1_' + str(i)) for i in range(wy)]

        m = self.Model(wy)
        eqs = []
        for i in range(wy):
            # x=x0
            eqs.append(m.diff(i).subs({m.x: 0}) - y0[i])
            # x=x1
            eqs.append(m.diff(i).subs({m.x: m.x1}) - y1[i])
        sol = sympy.solve(eqs, *m.c)
        cse_defs, code_block = self.get_cse_code(
            sol, 'cse')

        end_block = []
        for ci in m.c:
            code = self.as_arrayified_code(sol[ci])
            c_var = self.as_arrayified_code(ci)
            end_block.append('{} = {};'.format(c_var, code))

        return{
            'max_wy': self.max_wy,
            'max_deriv': self.max_deriv,
            'eval_scalar_expr': None,
            'eval_deriv_exprs': None,
            'coeff_cses': None,
            'coeff_exprs_in_cse': None,
            'coeff_end_exprs': None,
        }

    def variables(self):
        dd = defaultdict(dict)
        for wy in range(1, self.max_wy+1):
            d = self.variables_for_wy(wy)
            for k,v in d.items():
                dd[k][wy] = v

        dd.update({'SIZE_T': SIZE_T})
        return dd


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
