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

ST,ET=sp.symbols("ST,ET")
rs=1
re=1

pp = PdfPages('multipage.pdf')
for B in [1,2,3,4]:
	#B=1
	ST_dot=rs*(1-ST/ET)
	ET_dot=re*ET*(1-ET)-B/ST
	# define the system dy/dt = f(y, t)
	def f(X,t):
	   xval=X[0]
	   yval=X[1]
	   xdv=ST_dot.subs({ST:xval,ET:yval})
	   ydv=ET_dot.subs({ST:xval,ET:yval})
	   return([xdv,ydv])
	
	tf=np.linspace(0, 2, 20)   # time grid forward
	tb=np.linspace(0,-2, 20)   # time grid backwards
	ST_min= -0.5
	ST_max= max(1.5*abs(B),1)
	ET_min=-0.5
	ET_max= 0.5
	X = np.arange(ST_min, ST_max, .1)
	Y = np.arange(ET_min, ET_max, .1)
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
	    f1=plt.figure()
	    for solutionSet in data:
	        for soln in solutionSet:
	            xvals=soln[:,0]
	            yvals=soln[:,1]
	            plt.plot(xvals,yvals)
	    U= evalOnGrid(Xm,Ym,ST_dot,[ST,ET])
	    V =evalOnGrid(Xm,Ym,ET_dot,[ST,ET])
	    Q = plt.quiver( Xm,Ym, U, V,pivot="tip",units="width")
	    plt.title("B="+str(B))
	    plt.xlim(ST_min,ST_max)
	    plt.ylim(ET_min,ET_max)
	    pp.savefig(f1)
	else:
	    assert data is None

pp.close()
