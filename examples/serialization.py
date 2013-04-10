import numpy as np

from sine_curve import get_sin_pp

if __name__ == '__main__':
    pp = get_sin_pp()
    ori_t, ori_c = pp.t.copy(), pp.c.copy()
    pickle.dump(pp, open('sine_pp.pkl', 'wb'), protocol = 2)
    pp2 = pickle.load(open(save, 'rb'))
    assert np.allclose(pp2.t, ori_t) and \
           np.allclose(pp2.c, ori_c)
