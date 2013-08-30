#!/usr/bin/python
# vim: set expandtab ts=4

from mpi4py import MPI
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from matplotlib.backends.backend_pdf import PdfPages

def evalOnGrid(X,Y,expr):
    fpair=lambda xv,yv: expr.subs({x:xv,y:yv}).evalf()
    frows=lambda xrow,yrow:map(fpair,xrow,yrow)
    Z = np.array(map(frows,X,Y),dtype=float)
    return(Z)

x,y=sp.symbols("x,y")

pp = PdfPages('multipage.pdf')
#for mu in [-1,-0.5,0,0.5,1]:
for mu in [0.5]:
    # define the system
    x_dot=mu*x-x**2
    y_dot=-y
    
    # define the system dy/dt = f(y, t)
    def f(X,t):
       xval=X[0]
       yval=X[1]
       xdv=x_dot.subs({x:xval,y:yval})
       ydv=y_dot.subs({x:xval,y:yval})
       return([xdv,ydv])
    
    f1=plt.figure()
    tf=np.linspace(0, 4, 20)   # time grid forward
    tb=np.linspace(0, -4, 20)   # time grid backwards
    # create a cloud of initial values (tracectory starting points)
    # We chose a combination of 3 boundaries here
    
    x_min= -0.5
    x_max= 0.5
    y_min=-0.5
    y_max= 0.5
    x_max= max(1.5*abs(mu),1)
    X = np.arange(x_min, x_max, .1)
    Y = np.arange(y_min, y_max, .1)
    Xm, Ym = np.meshgrid(X, Y)
    startValues=[[i,j] for i in X for j in Y]
    #startValues=[[x_max,i] for i in Y ]\
    #+[[ 0.2,i] for i in Y ]\
    #+[[-0.2,i] for i in Y ]\
    #+[[ 0.2+mu,i] for i in Y ]\
    #+[[-0.2+mu,i] for i in Y ]\
    #+[[i, y_max] for i in np.linspace(-.1,max(1.5*abs(mu),1),5)] \
    #+[[i, y_min] for i in np.linspace(-.1,max(1.5*abs(mu),1),5)]
    for X0 in startValues:
        soln=odeint(f,X0,tf)
        xvals=soln[:,0]
        yvals=soln[:,1]
        plt.plot(xvals,yvals)
        soln=odeint(f,X0,tb)
        xvals=soln[:,0]
        yvals=soln[:,1]
        plt.plot(xvals,yvals)
    
    U= evalOnGrid(Xm,Ym,x_dot)
    V =evalOnGrid(Xm,Ym,y_dot)
    Q = plt.quiver( Xm,Ym, U, V,pivot="tip",units="width")
    #qk = plt.quiverkey(Q, 0.5, 0.92, 2, r'$2 \frac{m}{s}$', labelpos='W',
    #               fontproperties={'weight': 'bold'})
    plt.title("mu="+str(mu))
    plt.xlim(x_min,x_max)
    plt.ylim(y_min,y_max)
    #plt.show()
    pp.savefig(f1)
pp.close()
