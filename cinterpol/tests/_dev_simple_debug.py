import core
import numpy as np
import matplotlib.pyplot as plt

t=np.array([0.0,2.0,3.0,4.0,5.0],dtype=np.float64)
Y=np.vstack((np.sin(t),np.cos(t),-np.sin(t))).transpose()
pp=core.PiecewisePolynomial(t,Y)
print pp(t*0.5)-np.sin(t*0.5)
print pp(t*0.9)-np.sin(t*0.9)
print pp(t*0.99)-np.sin(t*0.99)
print pp(t*0.999)-np.sin(t*0.999)
print pp(t*0.9999)-np.sin(t*0.9999)
tfine=np.linspace(t[0],t[-1])
plt.plot(t, Y[:,0], '*', label = 'Data')
plt.plot(tfine, pp(tfine), label='Interpolated')
plt.show()
