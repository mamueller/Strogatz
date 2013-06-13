#!/usr/bin/python
# vim: set expandtab ts=4
import sympy as sp
from pylab import *
from numpy import ma

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


#Example spherical coordinates
x,y=sp.symbols("x,y")
X=x,y
xdot,ydot,rdot,phidot=sp.symbols("xdot,ydot,rdot,phidot")
XdotSym=sp.Matrix([xdot,ydot])
xdot=x-y-x*(x**2+5*y**2)
ydot=x+y-y*(x**2+y**2)
Xdot=sp.Matrix([xdot,ydot])
#plot it

Xv,Yv = meshgrid( arange(0,2*pi,.2),arange(0,2*pi,.2) )
Xdotv = cos(Xv)

print("\nThe system:\n")
sp.pprint(XdotSym)
print("=")
sp.pprint(Xdot)

r=sp.symbols("r",positive=True,real=True)
phi=sp.symbols("phi",real=True)
U=sp.Matrix([r,phi])
## then X(U) is given by:
x =  r*sp.cos(phi)
y =  r*sp.sin(phi)
XofU=sp.Matrix([x,y])
print("\nThe coordinate transformation:\n")
sp.pprint(XofU)
T1=Coords(X,U,XofU,sp.trigsimp)


print("\nThe Jacobian of the transformation:\n")
sp.pprint(T1.J)
print("\nThe inverse of the Jacobian :\n")
sp.pprint(T1.Jinv)

xdot=x-y-x*(x**2+5*y**2)
ydot=x+y-y*(x**2+y**2)
Xdot=sp.Matrix([xdot,ydot])
Udot=T1.matSimp(T1.Jinv*Xdot)
print("\nThe system in the new variables:\n")
sp.pprint(sp.Matrix([rdot,phidot]))
sp.pprint(Udot)
