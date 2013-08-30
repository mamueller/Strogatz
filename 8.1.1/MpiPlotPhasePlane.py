#!/usr/bin/python
# vim: set expandtab ts=4
from mpi4py import MPI
import numpy as np
import sympy as sp
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from evalOnGrid import evalOnGrid

comm = MPI.COMM_WORLD
size = comm.Get_size()
def myrange(myrank,arr):
    l=len(arr)
    slicewidth=l/size
    if myrank<size:
        res=arr[slicewidth*rank:slicewidth*(rank+1)]
    else:
        res=arr[slicewidth*rank:]
    return(res)

x,y=sp.symbols("x,y")
mu=1
x_dot=mu*x-x**2
y_dot=-y
# define the system dy/dt = f(y, t)
def f(X,t):
   xval=X[0]
   yval=X[1]
   xdv=x_dot.subs({x:xval,y:yval})
   ydv=y_dot.subs({x:xval,y:yval})
   return([xdv,ydv])

tf=np.linspace(0, 2, 20)   # time grid forward
tb=np.linspace(0,-2, 20)   # time grid backwards
x_min= -0.5
x_max= max(1.5*abs(mu),1)
y_min=-0.5
y_max= 0.5
X = np.arange(x_min, x_max, .1)
Y = np.arange(y_min, y_max, .1)
Xm, Ym = np.meshgrid(X, Y)
startValues=[[i,j] for i in X for j in Y]
rank = comm.Get_rank()
myStartValues=myrange(rank,startValues)
mydata=[]
for X0 in myStartValues:
    soln=odeint(f,X0,tf)
    mydata.append(soln)
    soln=odeint(f,X0,tb)
    mydata.append(soln)
#data = (rank+1)**2
data = comm.gather(mydata, root=0)
if rank == 0:
    print("rank="+str(rank))
    pp = PdfPages('multipage.pdf')
    f1=plt.figure()
    for solutionSet in data:
        for soln in solutionSet:
            xvals=soln[:,0]
            yvals=soln[:,1]
            plt.plot(xvals,yvals)
    U= evalOnGrid(Xm,Ym,x_dot,[x,y])
    V =evalOnGrid(Xm,Ym,y_dot,[x,y])
    Q = plt.quiver( Xm,Ym, U, V,pivot="tip",units="width")
    plt.title("mu="+str(mu))
    plt.xlim(x_min,x_max)
    plt.ylim(y_min,y_max)
    pp.savefig(f1)
    pp.close()
else:
    assert data is None

