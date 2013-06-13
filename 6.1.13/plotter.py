#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from sympy import *

c=10
PHI=np.linspace(0,np.pi*c*10,10000)
phi=symbols("phi")
phi_1=c*pi/2
phi_2=phi_1+2*pi
phi_3=phi_2+c*pi/2
r1=1
r=Piecewise((sin(phi/c),phi<=phi_1),(r1,phi_1<phi and phi<=phi_2),(r1+sin((phi-phi_2)/c),phi>phi_2 and phi<=phi_3))
fr=lambdify(phi,r)
R=map(fr,PHI)
plt.figure()
plt.plot(np.cos(PHI)*R,np.sin(PHI)*R)
plt.show()
