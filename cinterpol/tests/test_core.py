
import numpy as np
import matplotlib.pyplot as plt

from c_interpol import PieceWisePolyInterpol


def test_Traj():
    c = np.array([[1, 3, 2], [6.0, 0, 0]]) # y=1+3x+2*x**2
    t = np.array([0.0, 1.0])
    tj = Traj(t, c)
    print tj([0.0, 0.5, 1.0])

def test_Traj_mk_from_data():
    t = np.array([0.0, 1.0])
    y = np.array([[0.0, 0.0, 0.0],
                  [1.0, 3.0, 6.0]]) # y=x**3
    t = Traj.mk_from_data(t, y)
    print t.get_t()
    print t.get_c()
    plot_t = np.linspace(0, 1.0, 50)
    plot_y = t(plot_t)
    plt.plot(plot_t, plot_y, label = 'Interpol')
    plt.plot(plot_t, plot_t ** 3, label = 'Analytic', ls='--')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    test_Traj()
    test_Traj_mk_from_data()

