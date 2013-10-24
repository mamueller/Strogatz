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

x,y	=sp.symbols("x,y")
A,B,q	=sp.symbols("A,B,q")
par_sym=[A,B,q]

x_dot=B-x-(x*y)/(1+q*x**2)
y_dot=A-(x*y)/(1+q*x**2)
X=[x,y]
X_dot=[x_dot,y_dot]
# compute the jacobian
def dd(i,j):
    return(sp.diff(X_dot[i],X[j]))
n=2
J=sp.Matrix(2,2,dd)
Jdet=J.det()
xfix=B-A
yfix=A/(B-A)*(1+q*(B-A**2))
JdetFix=Jdet.subs({x:xfix,y:yfix})

rank = comm.Get_rank()
if rank == 0:
	print(J)
	print(Jdet)
	# define the fixed points
	print(xfix)
	print(yfix)
	print(JdetFix)
	pp = PdfPages('multipage.pdf')

############### start plotting ##############################################
qval=3

for parDict in [{A:1,B:2,q:qval},{A:1.2,B:1.8,q:qval},{A:1.4,B:1.6,q:qval},{A:1.5,B:1.5,q:qval}]:
	x_dot_par=x_dot.subs(parDict)
	y_dot_par=y_dot.subs(parDict)
	    
	# define the system dy/dt = f(y, t)
	def f(X,t):
	   xval=X[0]
	   yval=X[1]
	   xdv=x_dot_par.subs({x:xval,y:yval})
	   ydv=y_dot_par.subs({x:xval,y:yval})
	   return([xdv,ydv])
	
	tf=np.linspace(0, 2, 6)   # time grid forward
	tb=np.linspace(0,-2, 6)   # time grid backwards
	xfix_par=xfix.subs(parDict)
	yfix_par=yfix.subs(parDict)
	print(xfix_par)
	print(yfix_par)
	#x_min= xfix_par-1 
	#x_max= xfix_par+1
	#y_min= yfix_par-1
	#y_max= yfix_par+1
	x_min= 0
	x_max= 2
	y_min= 3
	y_max= 5
	X = np.arange(x_min, x_max, .25)
	Y = np.arange(y_min, y_max, .25)
	Xm, Ym = np.meshgrid(X, Y)
	startValues=[[i,j] for i in X for j in Y]
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
	    U= evalOnGrid(Xm,Ym,x_dot_par,[x,y])
	    V =evalOnGrid(Xm,Ym,y_dot_par,[x,y])
	    Q = plt.quiver( Xm,Ym, U, V,pivot="tip",units="width")
	    plt.title("A="+str(A))
	    plt.xlim(x_min,x_max)
	    plt.ylim(y_min,y_max)
	    pp.savefig(f1)
	else:
	    assert data is None
		
if rank == 0:
	pp.close()
