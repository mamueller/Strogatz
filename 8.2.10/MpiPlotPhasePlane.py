#!/usr/bin/python
# vim: set expandtab ts=4
from mpi4py import MPI
import numpy as np
import sympy as sp
from sympy import symbols,Matrix
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
C_S, C_B, C_0=symbols("C_S, C_B, C_0",real=True) 
C=Matrix(2,1,[C_S,C_B]) 

#respired carbon fraction
r=symbols("r") 

# a scalar representing the Activity factor;
# i.e. a temperature and moisture modifier (unitless)
A_f=symbols("A_f") 

# the michaelis constant 
K_m=symbols("K_m") 

#decay rates for (S)oil and (B)acteria
k_S, k_B =symbols("k_S, k_B") 

#input flux to pool S
ADD=symbols("ADD") 
# the alphas have to be a function of C and t (at most)
C_dot= Matrix([[-C_B*C_S*k_S/(C_S + K_m) + C_B*k_B], [C_B*C_S*k_S*(-r + 1)/(C_S + K_m) - C_B*k_B]])


