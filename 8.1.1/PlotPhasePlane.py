#!/usr/bin/python
# vim: set expandtab ts=4

import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('multipage.pdf')

def f2(X,Y,expr):
    fpair=lambda xv,yv: expr.subs({x:xv,y:yv}).evalf()
    frows=lambda xrow,yrow:map(fpair,xrow,yrow)
    Z = np.array(map(frows,X,Y),dtype=float)
    return(Z)
x,y=sp.symbols("x,y")

for mu in [-1,-0.5,0,0.5,1]:
    # define the system
    x_dot=mu*x-x**2
    y_dot=-y
    
    # solve the system dy/dt = f(y, t)
    def f(X,t):
       xval=X[0]
       yval=X[1]
       xdv=x_dot.subs({x:xval,y:yval})
       ydv=y_dot.subs({x:xval,y:yval})
       return([xdv,ydv])
    
    f1=plt.figure()
    t=np.linspace(0, 2.2, 20)   # time grid
    # create a cloud of initial values (tracectory starting points)
    # We chose a combination of 3 boundaries here
    
    x_min= -0.5
    x_max= 0.5
    y_min=-0.5
    y_max= 0.5
    Y = np.arange(y_min, y_max, .1)
    startvalues=[[x_max,i] for i in Y ]\
    +[[ 0.1,i] for i in Y ]\
    +[[-0.1,i] for i in Y ]\
    +[[ 0.1+mu,i] for i in Y ]\
    +[[-0.1+mu,i] for i in Y ]\
    +[[i, y_max] for i in np.linspace(-.1,max(1.5*abs(mu),1),5)] \
    +[[i, y_min] for i in np.linspace(-.1,max(1.5*abs(mu),1),5)]
    x_mins=[]
    for X0 in startvalues:
        soln=odeint(f,X0,t)
        xvals=soln[:,0]
	x_mins.append(min(xvals))
        yvals=soln[:,1]
        plt.plot(xvals,yvals)
    
    #x_min=min(x_mins)
    x_max= max(1.5*abs(mu),1)
    X = np.arange(x_min, x_max, .1)
    Y = np.arange(y_min, y_max, .1)
    Xm, Ym = np.meshgrid(X, Y)
    U= f2(Xm,Ym,x_dot)
    V =f2(Xm,Ym,y_dot)
    Q = plt.quiver( Xm,Ym, U, V,pivot="tip",units="width")
    #qk = plt.quiverkey(Q, 0.5, 0.92, 2, r'$2 \frac{m}{s}$', labelpos='W',
    #               fontproperties={'weight': 'bold'})
    plt.title("mu="+str(mu))
    plt.xlim(x_min,x_max)
    #plt.show()
    pp.savefig(f1)
pp.close()
