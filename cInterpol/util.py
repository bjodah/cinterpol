import sympy

class Polynomial(object):
    """
    Symbolic Polynomial class for use with Sympy
    """

    x = sympy.Symbol('x', real = True)

    def __init__(self, order=None, c=None):
        """
        If order is not specified it is determined through the
          length of c.
        If c is not specified it is assumed generic
        """
        if order:
            assert c == None
            self.order = order
            self.c = [sympy.Symbol('c_' + str(o), real = True) for \
                      o in range(self.order + 1)]
        else:
            self.order = len(c) - 1
            assert order == None or order == self.order
            assert c != None
            self.c = c


    def diff(self, deg):
        return self.expr.diff(self.x, deg)

    @property
    def expr(self):
        return sum([self.c[o]*self.x**o for o in range(self.order + 1)])


    def eval(self, x, deriv_order=0, to_float=True):
        try:
            iter(deriv_order)
            tmp = [self.diff(do).subs({self.x: x}) for do\
                    in deriv_order]
            if to_float: tmp = map(float, tmp)
            return tmp
        except TypeError:
            if to_float:
                return float(self.diff(deriv_order).subs({self.x: x}))
            else:
                return self.diff(deriv_order).subs({self.x: x})
