import numpy as np
from scipy.sparse import spdiags
import math
# horizontal velocity 10 m/s
# boundary conditions are based on what is the surface
# Do we need to assume that the surface top has the same velocities as if we hit the surface
# or could run multiple iterations to solve the missing points.
dz = 1
dx = 1

# Surface Funciton 10sin(pi x/25)
# Initial w 4picos(pi x/25)
# Initial dw its late when i type this but is it wrong to have it be 0?
# or at least until we figure out the surface feature since as it is there
# is a dw/dx but not dw/dz at layer 1 since flat plane

x0 = 0
xf = 250
z0 = 0
zf = 2500

nx = int((xf - x0)/dx)#edirt later
nz = int((zf - z0)/dz)

N = 0.9 # I can't remember whats an "N", is it an emoticon?
u = 10 

wMat = np.zeros([nx, nz+2])
wMat[:, 1] = 4 * math.pi * np.cos(math.pi* np.arange(x0, xf, dx) / 25)
wMat[:, 0] = wMat[:, 1]

data = np.array([-(dz**2 / dx**2)*np.ones(nx), 
                 (2*dz**2 / dx**2 - N**2 * dz**2 / u + 2)*np.ones(nx), 
                 -(dz**2 / dx**2)*np.ones(nx)])
diags = np.array([-1, 0, 1])
diffMat = spdiags(data, diags, nx, nx).toarray()
# For a looping boundary
diffMat[-1, 0] = -(dz**2 / dx**2)
diffMat[0, -1] = -(dz**2 / dx**2)
#


for z in np.arange(2, nz + 2):
    wMat[:, z] = np.matmul(diffMat,wMat[:, z-1].transpose()) - wMat[:, z-2]


# I have some idea involving absolute magnitude needs more thoguht though