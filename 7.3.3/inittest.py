#!/usr/bin/python
# vim: set expandtab ts=4

from sympy import *
class Initest(object):
    def __init__(self,var,fun):
        self.var=var
        self.fun=fun
        self.comp=fun(var)
        def matfun(Mat):
            s=Mat.shape
            res=zeros(s)
            for i in range (s[0]):
                for j in range (s[1]): 
                    res[i,j]=fun(Mat[i,j])
        self.matfun=matfun           
        self.mat=matfun(ones(2))

a=Initest(4,lambda x:x*2)
print(a.mat)
