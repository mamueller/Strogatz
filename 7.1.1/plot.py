#!/usr/bin/python
# vim: set expandtab ts=4
import sympy as sp
from Coords import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator , FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from helpers import *

R = np.arange(0, 5, .5)
PHI = np.arange(0, 2*sp.pi, .5)
R, PHI = np.meshgrid(R, PHI)


#Example spherical coordinates
x,y=sp.symbols("x,y")
X=x,y
xdot,ydot,rdot,phidot=sp.symbols("xdot,ydot,rdot,phidot")
XdotSym=sp.Matrix([xdot,ydot])
xdot=x-y-x*(x**2+5*y**2)
ydot=x+y-y*(x**2+y**2)
Xdot=sp.Matrix([xdot,ydot])
r=sp.symbols("r",positive=True,real=True)
phi=sp.symbols("phi",real=True)
U=sp.Matrix([r,phi])
## then X(U) is given by:
x =  r*sp.cos(phi)
y =  r*sp.sin(phi)
XofU=sp.Matrix([x,y])
print("\nThe coordinate transformation:\n")
sp.pprint(XofU)
T1=Coords(X,U,XofU,sp.trigsimp)
X,Y=T1.trans((R,PHI))
#X,Y=trans((R,PHI),(r,phi),x,y)


print("\nThe Jacobian of the transformation:\n")
sp.pprint(T1.J)
print("\nThe inverse of the Jacobian :\n")
sp.pprint(T1.Jinv)

xdot=x-y-x*(x**2+5*y**2)
ydot=x+y-y*(x**2+y**2)
Xdot=sp.Matrix([xdot,ydot])
Udot=T1.matSimp(T1.Jinv*Xdot)
print("\nThe system in the new variables:\n")
sp.pprint(sp.Matrix([rdot,phidot]))
sp.pprint(Udot)
