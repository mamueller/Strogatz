#!/usr/bin/python
# vim: set expandtab ts=4
import numpy as np
import sympy as sp
def evalOnGrid(X,Y,expr,symbols):
    x,y=symbols
    fpair=lambda xv,yv: expr.subs({x:xv,y:yv}).evalf()
    frows=lambda xrow,yrow:map(fpair,xrow,yrow)
    Z = np.array(map(frows,X,Y),dtype=float)
    return(Z)
