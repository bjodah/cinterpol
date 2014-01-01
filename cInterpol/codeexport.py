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


SIZE_T = 'int' # Change to 'size_t' if needed. (use os.environ.get?)

def cache(cb): # super simple cache
    res = {}
    def wrapper(self):
        if not self in res:
            res[self] = cb(self)
        return res[self]
    return wrapper

class ModelCode(C_Code):

    source_files = ['./cInterpol/coeff.c',
                    './cInterpol/eval.c']

    templates = ['./cInterpol/coeff_template.c',
                 './cInterpol/coeff_template.h',
                 './cInterpol/eval_template.c',
                 './cInterpol/eval_template.h',]

    def __init__(self, tokens, models, max_wy, *args, **kwargs):
        self.tokens = tokens
        self.models = models
        self.max_wy = max_wy
        super(ModelCode, self).__init__(*args, **kwargs)


    def variables_for_model_and_wy(self, Model, wy, max_deriv):
        # number of cofficients per peicewise segment
        wc = wy*2

        # Sympy variable symbols for formulating code
        y0 = [sympy.Symbol('y0_' + str(i)) for i in range(wy)]
        y1 = [sympy.Symbol('y1_' + str(i)) for i in range(wy)]

        m = Model(wy)

        # Expressions for evaluating function value (eval_template.c)
        # -----------------------------------------------------------
        eval_cse, eval_expr = {}, {}
        for i in range(max_deriv+1):
            eval_cse[i], eval_expr[i] = self.get_cse_code(m.expr.diff(m.x, i))
            # dummy_groups=(
            #     #DummyGroup('y_dummy', m.y),
            #     #DummyGroup('coeff_dummies', m.c),
            # ),
            # arrayify_groups=(
            #     #ArrayifyGroup('y_dummy', 'yout'),),
            #     #ArrayifyGroup('coeff_dummies', 'c'),),
            #)

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
            m.expr,
            dummy_groups=(
                DummyGroup('x_dummy', [m.x]),
            ),
            arrayify_groups=( # see coeff_template.c
                ArrayifyGroup('x_dummy', 'dt'),
            ),
        )


        coeff_end_exprs = []
        for ci in m.c:
            code = self.as_arrayified_code(sol[ci])
            coeff_end_exprs.append(code)

        return{
            'eval_cse': eval_cse,
            'eval_expr': eval_expr,
            'coeff_cse': coeff_cse,
            'coeff_expr': coeff_expr,
            'coeff_end_exprs': coeff_end_exprs,
        }

    @cache
    def variables(self):
        # Variables passed on to {coeff,eval}_template.{c,h} and piecewise_template.pyx
        d=defaultdict(lambda: defaultdict(dict)) # allows to assign d['a']['b']['c'] = 3
        d['max_deriv'] = {wy: wy*2-1 for wy in range(1,self.max_wy+1)}
        for token, Model in zip(self.tokens, self.models):
            for wy in range(1, self.max_wy+1):
                dd = self.variables_for_model_and_wy(Model, wy, d['max_deriv'][wy])
                for k, v in dd.items():
                    d[k][token][wy] = v

        for k1,v in d.items():
            if k1 == 'max_deriv':
                print("[{}] = {}".format(k1,v))
                continue
            for k2,vv in v.items():
                for k3,vvv in vv.items():
                    print("[{}][{}][{}] = {}".format(k1,k2,k3,vvv))

        d['max_wy'] = self.max_wy
        d['SIZE_T'] = SIZE_T
        d['tokens'] = self.tokens
        return d
