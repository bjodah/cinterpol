import numpy as np

from sine_curve import get_sin_pp, plot

if __name__ == '__main__':
    pp = get_sin_pp()
    t0,tend = pp.t[0], pp.t[-1]
    span=tend-t0
    plot(pp, 0, t0-span*0.2, tend+span*0.2)
