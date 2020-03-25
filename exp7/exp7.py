from sympy import *
import scipy.signal as sp
import pylab as pp

def lowpass(R1, R2, C1, C2, G, Vi):
	s = symbols('s')
	A = Matrix([[0, 0, 1, -1 / G], [-1 / (1 + s * R2 * C2), 1, 0, 0], [0, -G, G, 1], [-1 / R1 - 1 / R2 - s * C1, 1 / R2, 0, s * C2]])
	b = Matrix([0, 0, 0, -Vi / R1])
	V = A.inv() * b
	return A, b, V

def expToLTI(X):
	print(X)
	X = expand(simplify(X))
	n, d = fraction(X)
	n, d = Poly(n, symbols('s')).all_coeffs(), Poly(d, symbols('s')).all_coeffs()
	n, d = [float(f) for f in n], [float (f) for f in d]
	d.append(0)
	print(n, d)
	return sp.lti(n, d)

# Step response of lowpass filter
A, b, V = lowpass(1e4, 1e4, 1e-9, 1e-9, 1.586, 1)
H = expToLTI(V[3])
# t, x = sp.step(H, T = pp.linspace(0, 1e-3, 10000))
# pp.plot(t, x)
# pp.show()
H = sp.lti([1], [1e-12, 1e-4, 1])

# Output of given signal
v = lambda t : (cos(1e3*t) - cos(1e6*t)) * (t > 0)
t = pp.linspace(0, 30e-6, int(1e5 + 1))
t, x, _ = sp.lsim(H, v(t), t)
plot(t, x)
show()
