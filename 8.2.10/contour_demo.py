#!/usr/bin/env python
"""
Illustrate simple contour plotting, contours on an image with
a colorbar for the contours, and labelled contours.

See also contour_image.py.
"""
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

delta = 0.025
x = np.arange(-5.0, 5.0, delta)
y = np.arange(-5.0, 5.0, delta)
X, Y = np.meshgrid(x, y)
#Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
#Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
## difference of Gaussians
#Z = 10.0 * (Z2 - Z1)
Z=np.sqrt(X**2+Y**2)



# Create a simple contour plot with labels using default colors.  The
# inline argument to clabel will control whether the labels are draw
# over the line segments of the contour, removing the lines beneath
# the label
fig=plt.figure()
pl1=fig.add_subplot(2,1,1)
CS1 =pl1.contourf(X, Y, Z,levels=[0,1,2],colors=["b","r"])
CS = pl1.contour(X, Y, Z,levels=[0,1,2],colors=["b","r"])
plt.clabel(CS, inline=1, fontsize=10)
plt.title('Simplest default with labels')

#now as overlay 
pl1=fig.add_subplot(2,1,2)
CS1 =pl1.contourf(X, Y, Z,levels=[0,1],alpha=.5,colors=["b"])
CS1 =pl1.contourf(X, Y, Z,levels=[0,2],alpha=.5,colors=["r"])
CS =pl1.contour(X, Y, Z,levels=[0,1,2],colors=["b","r"])
plt.clabel(CS, inline=1, fontsize=10)


plt.show()
