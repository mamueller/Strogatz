#!/usr/bin/python
# vim: set expandtab ts=4
import sympy as sp
from helpers import *

class Coords(object):

    def __init__(self,X,U,XofU,scalarSimp):
        self.X=X
        self.U=U
        self.XofU=XofU
        self.n=len(self.X)
        self.scalarSimp=scalarSimp
        self.setup()
        
    def matSimp(self,Mat):
        s=Mat.shape
        res=sp.zeros(s)
        for i in range (s[0]):
            for j in range (s[1]): 
                res[i,j]=sp.simplify(self.scalarSimp(Mat[i,j]))
        return(res)
    def setup(self):
        def dd(i,j):
            return(sp.diff(self.XofU[i],self.U[j]))
        
        self.J=sp.Matrix(self.n,self.n,dd)
        J=self.J.inv()
        self.Jinv=self.matSimp(self.J.inv())
   
    def trans(self,arraytupel):
        symboltupel=self.U[0],self.U[1]
        x_exp=self.XofU[0]
        y_exp=self.XofU[1]
        X=mapExpression(arraytupel,symboltupel,x_exp)
        Y=mapExpression(arraytupel,symboltupel,y_exp)
        return(X,Y)


