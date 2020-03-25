from PIL import Image
from pylab import *
import mpl_toolkits.mplot3d.axes3d as p3
import scipy.linalg as lg
import sys
import copy

def estimateExponent(vec):
	A = array([[1, x] for x in range(len(vec))])
	x = lg.lstsq(A, log(vec))[0]
	return exp(x[0]), x[1]

try:
	Nx = int(sys.argv[1])
except IndexError:
	Nx = 25
try:
	Ny = int(sys.argv[2])
except IndexError:
	Ny = 25
try:
	radius = int(sys.argv[3])
except IndexError:
	radius = 8
try:
	Niter = int(sys.argv[4])
except IndexError:
	Niter = 2500

# initial steps
x, y = linspace(-(Nx - 1) / 2, (Nx - 1) / 2, Nx), linspace(-(Ny - 1) / 2, (Ny - 1) / 2, Ny)
Y, X = meshgrid(y, x)

phi = zeros((Nx, Ny))

ii = where(X * X + Y * Y <= radius ** 2)
phi[ii] = 1.0
errors = []

for _ in range(Niter):

	oldphi = copy.copy(phi) # Copying
	oldphi = pad(oldphi, 1, 'edge') # Padding boundary values

	phi = 0.25 * (oldphi[:-2, 1:-1] + oldphi[1:-1, 2:] + oldphi[2:, 1:-1] + oldphi[1:-1, :-2])

	phi[ii] = 1.0 # Boundary conditions
	phi[0, :] = 0.0

	error = abs(phi - oldphi[1:-1, 1:-1]).max()
	if (error == 0.0):
		print('Hi')
		break
	errors.append(error)

# contour plot
contour(y, x, phi, levels = 20)
scatter(ii[0] - (Nx - 1) / 2, ii[1] - (Ny - 1) / 2, color = 'r', s = 10)
xlabel('x')
ylabel('y')
title('Contour of potential')
show()

# estimating exponential parameters
A1, B1 = estimateExponent(errors[500:])
A2, B2 = estimateExponent(errors)
K = range(Niter - 500)
L = range(500, Niter)
plot(L, errors[500:], label = 'errors')
plot(L, [A1 * exp(B1 * k) for k in K], label = 'fit1')
plot(L, [A2 * exp(B2 * k) for k in K], label = 'fit2')
legend()
show()

# making the 3d plot
ax = p3.Axes3D(figure(4))
title('The 3-D surface plot of the potential')
surf = ax.plot_surface(Y, X, phi, rstride = 1, cstride = 1, cmap = cm.jet, linewidth = 0, antialiased = True)
show()

# finding current densities
Jy = -0.5 * (oldphi[1:-1, 2:] - oldphi[1:-1, :-2])
Jx = -0.5 * (oldphi[2:, 1:-1] - oldphi[:-2, 1:-1])

quiver(y, x, Jy, Jx, scale = 5)
scatter(ii[0] - (Nx - 1) / 2, ii[1] - (Ny - 1) / 2, color = 'r', s = 10)
gca().set_aspect('equal', adjustable = 'box')
show()
