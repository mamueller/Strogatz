#!/usr/bin/python
# vim: set expandtab ts=4
import sympy as sp
import numpy as np
def mapExpression((Arr1,Arr2),(symbol1,symbol2),expr):
    fpair=lambda numval1,numval2: expr.subs({symbol1:numval1,symbol2:numval2}).evalf()
    frows=lambda xrow,yrow:map(fpair,xrow,yrow)
    Z = np.array(map(frows,Arr1,Arr2),dtype=float)
    return(Z)
