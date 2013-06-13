#!/usr/bin/python
from sympy import *
x,r,h=symbols("x,r,h")
r=3*x**2
h=-2*x**3
#find the minimum
dh=diff(h,x)
dh
x0=solve(dh,x)
x0
dr=diff(r,x)
dr
x0=solve(dr,x)
x0
