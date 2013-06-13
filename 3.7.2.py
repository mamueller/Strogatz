#!/usr/bin/python
from sympy import *
x,r,k=symbols("x,r,k")
r=x**3/(1+x**2)**2
k=2*x**3/(x**2-1)
#find the minimum
dk=diff(k,x)
x0=solve(dk,x)
x0
dr=diff(r,x)
x0=solve(dr,x)
x0
