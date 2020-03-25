import sys
import scipy.special as sp
import scipy.linalg as lg
from pylab import *

def g(x, a, b):
	return a * sp.jn(2,x) + b * x

if (len(sys.argv) < 2):
	print('Please enter question number as argument')
	print('3, 4\t - display all curves in one plot')
	print('5\t - display the errorbar')
	print('6\t - calculating M.p')
	print('7, 8\t - contour plot')
	print('9\t - estimating A B using linalg')
	print('9e\t - estimating A B without linalg')
	print('10\t - plot of error in estimating')
	print('11\t - loglog plot of error in estimating')
	print('all\t - print every result')

	exit()
else:
	mode = sys.argv[1]

# Read 2
a = transpose(loadtxt('fitting.dat'))
x, y = a[0], a[1:]
scl = logspace(-1, -3, 9)

# True value 4
y = vstack((y, array([g(t, 1.05, -0.105) for t in x])))

# Display 3
if mode in ('3', '4', 'all'):
	for i in range(9):
		plot(x, y[i], label = scl[i])
	plot(x, y[9], label = 'true value')
	legend()
	show()

# Errorbar 5
if mode in ('5', 'all'):
	i = 0
	plot(x, y[i], label = scl[i])
	plot(x, y[9], label = 'true value')
	errorbar(x[::5], y[i][::5], scl[i], fmt = 'ro')
	legend()
	show()

# Matrix 6
if mode in ('6', 'all'):
	M = array([[sp.jn(2, t), t] for t in x])
	p = array([1.05, -0.105])
	print("M = ", end = '')
	print(M)
	print("p = ", end = '')
	print(p)
	print("Sum of squared differences = ", end = '')
	print(((dot(M, p) - y[9])**2).sum())

# Contour 7, 8
if mode in ('7', '8', 'all'):
	A = arange(0, 2, 0.1)
	B = arange(-0.2, 0, 0.01)
	E = [[sum([(y[0][k] - g(x[k], i, j))**2 for k in range(101)]) / 101.0 for j in B] for i in A]
	clabel(contour(A, B, E, levels = 20))
	xlabel('A')
	ylabel('B')
	title('Contour of Error ij')
	show()

# Solve 9,extra
if mode in ('9e', 'all'):
	A = array([[sp.jn(2, i), i] for i in x])
	At = transpose(A)
	solution = array([list(linalg.solve(dot(At, A), dot(At, b))) for b in y])
	print('Solutions without linalg:')
	print(solution)

# Solve 9
if mode in ('9', '10','11', 'all'):
	M = array([[sp.jn(2, t), t] for t in x])
	solution = array([list(lg.lstsq(M, b)[0]) for b in y])
	if mode in ('9', 'all'):
		print('Solutions using linalg:')
		print(solution)

# Error in estimate 10
if mode in ('10', '11', 'all'):
	error = array([[(t[0] - 1.05)**2, (t[1] + 0.105)**2] for t in solution[:-1]])
	if mode != '11':
		plot(scl, error[:, 0], label = 'A')
		plot(scl, error[:, 1], label = 'B')
		legend()
		title('error vs stdev')
		show()
	if mode != '10':
		loglog(scl, error[:, 0], label = 'A')
		loglog(scl, error[:, 1], label = 'B')
		legend()
		title('loglog error vs stdev')
		show()
