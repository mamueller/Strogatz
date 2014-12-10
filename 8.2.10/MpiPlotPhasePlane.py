#!/usr/bin/python
# vim: set expandtab ts=4
from mpi4py import MPI
import numpy as np
import sympy as sp
from PhasePlanePlot import plotPhasePlane

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

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
if rank == 0:
    print(J)
    print(Jdet)
    # define the fixed points
    print("The coordinates of the fixed points")
    print("x="+str(xfix))
    print("y="+str(yfix))
    print("The determinant of the Jacobian")
    print(JdetFix)

qval=3
#for parDict in [{A:1,B:2,q:qval},{A:1.2,B:1.8,q:qval}]:
for parDict in [{A:1,B:2,q:qval}]:
    plotPhasePlane(parDict,X,X_dot)
##########################################################################
##########################################################################
C_0,t =symbols("C_0, t")
C1,C2=symbols("C1,C2",real=True,nonnegative=True)
i1,i2=symbols("i1,i2",real=True,nonnegative=True)
epsilon1,epsilon2=symbols("epsilon1,epsilon2",real=True,nonnegative=True)
t_start,t_end,tn=symbols("t_start,t_end,tn") 
#a1=i1
#a2=i2
C=Matrix(1,1,[C1])
F=Matrix([C1*(sin(C1)+1+epsilon1)])
I=Matrix(1,1,[i1])
pprint(I)
alphas={}
Model=RExample(C,alphas,F,I,"positiveEigenvalueOfJacobian")
#Css=sol[1]
#M.suggestFixedPoint( {C1:0.876085889442093,C2:0.876085889442093})

ranges=[[0,100]]
vectors=[ linspace(l[0],l[1],10) for l in ranges] 
startValues=tuplelist(vectors)
dic={ 
    epsilon1:0.4,
    epsilon2:0.1,
    i1:10,
    i2:10,
    # the following always have to be present
    C_0:Matrix(1,1,[1]),
    t_start:0,
    t_end:10,
    tn:100 ,
    # the following are needed if a numerical search for fixedpoints is to be conducted
    "startValuesForFixedPointSearch":startValues,   
    "plotRanges":ranges
	}

