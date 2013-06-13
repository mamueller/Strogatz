#!/usr/bin/python
# vim: set expandtab ts=4
from sympy import *

xdot,ydot,x,y=symbols("xdot,ydot,x,y")
xdot=x-y-x**3
ydot=x+y-y**3
J=Matrix([[diff(xdot,x),diff(xdot,y)],[diff(ydot,x),diff(ydot,y)]])
print(J)
J0=J.subs({x:0,y:0})
tau=J0.trace()
Delta=J0.det()
print(J0,tau,Delta)

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
        res=zeros(s)
        for i in range (s[0]):
            for j in range (s[1]): 
                res[i,j]=simplify(self.scalarSimp(Mat[i,j]))
        return(res)
    def setup(self):
        def dd(i,j):
            return(diff(self.XofU[i],self.U[j]))
        self.J=Matrix(self.n,self.n,dd)
        self.Jinv=self.matSimp(self.J.inv())


#Example spherical coordinates
x,y=symbols("x,y")
X=x,y
xdot,ydot,rdot,phidot=symbols("xdot,ydot,rdot,phidot")
XdotSym=Matrix([xdot,ydot])

xdot=x-y-x**3
ydot=x+y-y**3
Xdot=Matrix([xdot,ydot])
print("\nThe system:\n")
pprint(XdotSym)
print("=")
pprint(Xdot)

r=symbols("r",positive=True,real=True)
phi=symbols("phi",real=True)
U=Matrix([r,phi])

# then X(U) is given by:
x =  r*cos(phi)
y =  r*sin(phi)
XofU=Matrix([x,y])
print("\nThe coordinate transformation:\n")
pprint(XofU)
T1=Coords(X,U,XofU,trigsimp)


print("\nThe Jacobian of the transformation:\n")
print(T1.J)
print("\nThe inverse of the Jacobian :\n")
print(T1.Jinv)

xdot=x-y-x**3
ydot=x+y-y**3
Xdot=Matrix([xdot,ydot])
Udot=T1.matSimp(T1.Jinv*Xdot)
print("\nThe system in the new variables:\n")
pprint(Matrix([rdot,phidot]))
pprint(Udot)
