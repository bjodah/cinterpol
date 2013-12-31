# -*- coding: utf-8 -*-

# stdlib imports
import sympy
import re
from collections import defaultdict

# external imports
from pycompilation.codeexport import C_Code, DummyGroup, ArrayifyGroup
from pycompilation.util import render_mako_template_to

# project internal imports
from cInterpol.model import models


SIZE_T = 'int' # Change to 'size_t' if needed. (read ENV VAR?)

class ModelCode(C_Code):

    source_files = ['coeff.c',
                    'eval.c']

    templates = ['./cInterpol/coeff_template.c',
                 './cInterpol/coeff_template.h',
                 './cInterpol/eval_template.c',
                 './cInterpol/eval_template.h',]

    def __init__(self, Model, max_wy, max_deriv, *args, **kwargs):
        self.max_wy = max_wy
        self.max_deriv = max_deriv
        self.Model = Model
        super(ModelCode, self).__init__(*args, **kwargs)


    def variables_for_wy(self, wy):
        # number of cofficients per peicewise segment
        wc = wy*2

        # Sympy variable symbols for formulating code
        y0 = [sympy.Symbol('y0_' + str(i)) for i in range(wy)]
        y1 = [sympy.Symbol('y1_' + str(i)) for i in range(wy)]

        m = self.Model(wy)

        # Expressions for evaluating function value (eval_template.c)
        # -----------------------------------------------------------
        eval_cse, eval_expr = self.get_cse_code(
            sympy.Eq(m.expr),
            # dummy_groups=(
            #     #DummyGroup('y_dummy', m.y),
            #     #DummyGroup('coeff_dummies', m.c),
            # ),
            # arrayify_groups=(
            #     #ArrayifyGroup('y_dummy', 'yout'),),
            #     #ArrayifyGroup('coeff_dummies', 'c'),),
        )

        # Expressions for determinigs coefficients (coeff_template.c)
        # -----------------------------------------------------------
        eqs = []
        for i in range(wy):
            # x=x0
            eqs.append(m.diff(i).subs({m.x: m.x0}) - y0[i])
            # x=x1
            eqs.append(m.diff(i).subs({m.x: m.x1}) - y1[i])
        sol = sympy.solve(eqs, *m.c)

        coeff_cse, coeff_expr = self.get_cse_code(
            sol,
            sympy.Eq(m.expr),
            dummy_groups=(
                DummyGroup('x_dummy', [m.x]),
                DummyGroup('y_dummy', [m.y]),
            ),
            arrayify_groups=( # see coeff_template.c
                ArrayifyGroup('x_dummy', 'dt'),
                ArrayifyGroup('y_dummy', 'y', 'i*WY'),),
            )
        )

        coeff_end_exprs = []
        for ci in m.c:
            code = self.as_arrayified_code(sol[ci])
            coeff_end_exprs.append(code)

        return{
            'max_wy': self.max_wy,
            'max_deriv': self.max_deriv,
            'eval_scalar_expr': None,
            'eval_deriv_exprs': None,
            'coeff_cse': coeff_cse,
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
