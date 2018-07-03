# -*- coding: utf-8 -*-

import sympy

class Relation(object):

    expr = None
    x = sympy.Symbol('x', real = True)
    x0 = sympy.symbols('x0', real = True)
    x1 = sympy.symbols('x1', real = True)


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
            self.wy = len(c) // 2
            self.c = c


    def diff(self, deg):
        return self.expr.diff(self.x, deg)


    # Below are properties to be subclassed
    @property
    def expr(self):
        pass

    def eval(self, x_val, deriv=0):
        return self.expr.diff(self.x, deriv).subs({self.x: x_val})


class Polynomial(Relation):
    """
    Symbolic Polynomial class for use with Sympy
    """

    x0 = 0 # shifted polynomial

    @property
    def expr(self):
        return sum([self.c[o]*self.x**o for\
                    o in range(self.wy*2)])


class LinearCombination(Relation):

    @property
    def expr(self):
        l1 = [(self.x1-self.x)/self.x1*self.c[o]*self.x**o for \
              o in range(self.wy)]
        l2 = [self.x/self.x1*self.c[self.wy+o]*self.x**o for \
              o in range(self.wy)]
        return sum(l1+l2)


class Pade(Relation):

    @property
    def expr(self):
        l1 = sum([self.c[o]*self.x**o for o in range(self.wy+1)])
        l2 = sum([self.c[self.wy+o]*self.x**o for o in range(1, self.wy)])
        return l1/(1+l2)


models = {'poly': Polynomial,
          'lincomb': LinearCombination,
          'pade': Pade}
