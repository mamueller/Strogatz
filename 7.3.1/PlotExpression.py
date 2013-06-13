#!/usr/bin/python
# vim: set expandtab ts=4
import sympy as sp

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator , FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

def f1(X,Y):
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    return(Z)
def f2(X,Y,expr):
    fpair=lambda xv,yv: expr.subs({x:xv,y:yv}).evalf()
    frows=lambda xrow,yrow:map(fpair,xrow,yrow)
    Z = np.array(map(frows,X,Y),dtype=float)
    return(Z)
    
fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(-5, 5, 1)
Y = np.arange(-5, 5, 1)
X, Y = np.meshgrid(X, Y)
Z1 = f1(X,Y)
print(Z1)
x,y=sp.symbols("x,y")
ex=sp.sin(sp.sqrt(x**2+y**2))
Z2 = f2(X,Y,ex)
print(Z2)
#surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
#        linewidth=0, antialiased=False)
surf = ax.plot_surface(X, Y, Z2)
ax.set_zlim(-1.01, 1.01)

#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

#fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
