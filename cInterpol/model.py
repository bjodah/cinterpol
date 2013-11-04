import sympy

class Relation(object):

    expr = None
    x = sympy.Symbol('x', real = True)
    xend = sympy.symbols('xend')


    def __init__(self, wy=None, c=None):
        """
        If order is not specified it is determined through the
          length of c.
        If c is not specified it is assumed generic
        """
        if wy:
            assert c == None
            self.wy = wy
            self.c = [sympy.Symbol('c_' + str(o), real = True) for \
                      o in range(self.wy*2)]
        else:
            assert c != None
            self.wy = len(c) / 2
            self.c = c


    def diff(self, deg):
        return self.expr.diff(self.x, deg)


    # def eval(self, x, deriv_order=0, to_float=True):
    #     try:
    #         iter(deriv_order)
    #         tmp = [self.diff(do).subs({self.x: x}) for do\
    #                 in deriv_order]
    #         if to_float: tmp = map(float, tmp)
    #         return tmp
    #     except TypeError:
    #         if to_float:
    #             return float(self.diff(deriv_order).subs({self.x: x}))
    #         else:
    #             return self.diff(deriv_order).subs({self.x: x})

    # Below are properties to be subclassed
    @property
    def expr(self):
        pass



class Polynomial(Relation):
    """
    Symbolic Polynomial class for use with Sympy
    """

    @property
    def expr(self):
        return sum([self.c[o]*self.x**o for\
                    o in range(self.wy*2)])

class LinearCombination(Relation):

    @property
    def expr(self):
        l1 = [(1-self.x)*self.c[o]*self.x**o for \
              o in range(self.wy)]
        l2 = [self.x*self.c[self.wy+o]*(self.x-self.xend)**o for \
              o in range(self.wy)]
        return sum(l1+l2)

class Pade(Relation):

    @property
    def expr(self):
        l1 = sum([self.c[o]*self.x**o for\
                    o in range(self.wy+1)])
        l2 = sum([self.c[self.wy+1+o]*self.x**o for\
                    o in range(1,self.wy)])
        return sum(l1)/sum(1+l2)


models = {'poly': Polynomial,
          'lincomb': LinearCombination,
          'pade': Pade}
