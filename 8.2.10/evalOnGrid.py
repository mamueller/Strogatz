#!/usr/bin/python3
# vim: set expandtab ts=4
import numpy as np
from sympy import lambdify
def evalOnGrid(X,Y,expr,symbols):
    x,y=symbols
    f=lambdify((x,y),expr,"numpy")
    #fpair=lambda xv,yv: expr.subs({x:xv,y:yv}).evalf()
    #frows=lambda xrow,yrow:map(fpair,xrow,yrow)
    #Z = np.array(map(frows,X,Y),dtype=float)
    Z=f(X,Y)
    return(Z)
