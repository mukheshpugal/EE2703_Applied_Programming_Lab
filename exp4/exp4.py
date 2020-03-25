import numpy as np
from pylab import *
from scipy.integrate import quad
import scipy.linalg as lg
import sys

if (len(sys.argv) < 2):
	print('Please enter question number as argument')
	print('1\t - finding fourier coefficients by integration')
	print('2\t - reconstructing the function using fourier coefficients')
	print('3\t - displaying the coefficients obtained by integration')
	print('4\t - finding fourier coefficients by least squares')
	print('5\t - displaying the coefficients obtained by least squares')
	print('6\t - displaying the difference in estimates')
	print('7\t - displaying A.c')
	print('all\t - print every result')

	exit()
else:
	mode = sys.argv[1]

# Reconstructs function using fourier coefficients

def reconstruct(x, coeffs):
	return sum([coeffs[n][0] * cos(n * x) + coeffs[n][1] * sin(n * x) for n in range(len(coeffs))])

# Add functions to this list

functions = []
functions.append(lambda x : exp(x))
functions.append(lambda x : cos(cos(x)))
# functions.append(lambda x : x**2)
# functions.append(lambda x : 0 if x < pi else 1)

for f in functions:

	# By integration
	if mode in ('1', '2', '3', '6', 'all'):

		fourierFuncs = [lambda x, n : f(x) * cos(x * n), lambda x, n : f(x) * sin(x * n)]

		# using quad to integrate
		fourierCoeffs = array([[quad(fourierFuncs[i], 0, 2 * pi, args = (n))[0] / pi for i in range(2)] for n in range(26)])
		fourierCoeffs[0][0] /= 2

		if mode in ('1', 'all'):
			x0 = linspace(-2 * pi, 4 * pi, 400)
			y0 = [f(x) for x in x0]
			semilogy(x0, y0)
			show()

		X = linspace(0, 2 * pi, 100)

		Y = [reconstruct(x, fourierCoeffs) for x in X]
		Yo = [f(x) for x in X]

		# Displaying fourier coefficients
		if mode in ('3', 'all'):
			loglog(fourierCoeffs[:, 0], 'r.', label = 'a')
			loglog(fourierCoeffs[:, 1], 'r.', label = 'b')
			legend()
			show()

		# Displaying reconstructed graph
		if mode in ('2', 'all'):
			plot(X, Y, label = 'fourier')
			plot(X, Yo, label = 'original')
			legend()
			show()

	# By least squares estimation
	if mode in ('4', '5', '6', '7', 'all'):
		X = linspace(0, 2 * pi, 100)

		# Creating M and b
		M = array([hstack((array([1]), (array([array([cos(n * x), sin(n * x)]) for n in range(1, 26)])).flatten())) for x in X])
		b = [f(x) for x in X]

		a = lg.lstsq(M, b)[0]

		# Converting coefficients to readable form
		cf = [[a[0], 0]]
		for i in range(1, int((len(a) + 1) / 2)):
			cf.append([a[2 * i - 1], a[2 * i]])
		cf = array(cf)

		# Displaying reconstructed function
		if mode in ('4', '7', 'all'):
			y = [reconstruct(x, cf) for x in X]
			yo = [f(x) for x in X]
			if mode == '7':
				plot(X, yo, 'b', label = 'original')
				plot(X, y, 'g.', label = 'fourier')
				legend()
				show()
			if mode != '7':
				plot(X, y, label = 'fourier')
				plot(X, yo, label = 'original')
				legend()
				show()

		# Displaying coefficients
		if mode in ('5', 'all'):
			plot(cf[:, 0], label = 'a')
			plot(cf[:, 1], label = 'b')
			legend()
			show()

		# Displaying error in estimation
		if mode in ('6', 'all'):
			diff = subtract(cf, fourierCoeffs)
			plot(diff[:, 0], label = 'a')
			plot(diff[:, 1], label = 'b')
			legend()
			show()