#!/usr/bin/python
# we want to produce a circular vercor field
import matplotlib.pyplot as plt
import numpy as np
from sympy import *
def plotField(M):
    x,y=symbols("x,y")
    X=Matrix([x,y])
    Xdot=M*X
    xdot,ydot=Xdot
    xdotfunc=lambdify((x,y),xdot)
    ydotfunc=lambdify((x,y),ydot)
    xvals,yvals = np.meshgrid( np.arange(-10,10),np.arange(-10,10) )
    plt.quiver(xvals,yvals,xdotfunc(xvals,yvals),ydotfunc(xvals,yvals))

def plotNormedField(M):
    x,y=symbols("x,y",real=True)
    X=Matrix([x,y])
    Xdot=M*X
    xdot,ydot=Xdot
    xdotfunc=lambdify((x,y),xdot)
    ydotfunc=lambdify((x,y),ydot)
    xvals,yvals = np.meshgrid( np.arange(-10,10,.3),np.arange(-10,10,.3) )
    xv=xdotfunc(xvals,yvals)
    yv=ydotfunc(xvals,yvals)
    n=np.sqrt(xv**2+yv**2)
    plt.quiver(xvals,yvals,xv/n,yv/n)

M=Matrix([[1,5],[2,3]])
plt.figure
plotField(M)
plotNormedField(M)
plt.savefig("quiver.pdf", format='pdf')
