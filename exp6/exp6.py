from pylab import *
import scipy.signal as sp
import sys

def spring(freq, dec):
	num = poly1d([1, dec])
	den = poly1d([1, 2 * dec, dec**2 + freq**2])
	den = polymul([1, 0, 2.25], den)
	return sp.lti(num, den)

# Solving for forced response
t, x = sp.step(spring(1.5, 0.5), None, linspace(0, 50, 5001))
plot(t, x)
show()

t, x = sp.impulse(spring(1.5, 0.05), None, linspace(0, 50, 5001))
plot(t, x)
show()

# Forced response of different frequencies
l = []
for f in linspace(1.4, 1.6, 5):
	H = sp.lti([1], [1, 0, 2.25])
	t = linspace(0, 150, 5001)
	u = cos(f * t) * exp(-0.05 * t) * (t > 0)
	t, x, _ = sp.lsim(H, u, t)
	plot(t, x)
	l.append('freq : ' + str(f))

legend(l)
show()

# Coupled differential equations
X = sp.lti([1, 0, 2], [1, 0, 3, 0])
t, x = sp.impulse(X, None, linspace(0, 20, 2001))
plot(t, x)

Y = sp.lti([2], [1, 0, 3, 0])
t, y = sp.impulse(Y, None, linspace(0, 20, 2001))
plot(t, y)
show()

# Transfer function of two port network
H = sp.lti([1], [1e-12, 1e-4, 1])
w, S, phi = H.bode()
subplot(2, 1, 1)
semilogx(w, S)
subplot(2, 1, 2)
semilogx(w, phi)
show()

# Solving for two port network
v = lambda t : (cos(1e3*t) - cos(1e6*t)) * (t > 0)
t = linspace(0, 30e-6, int(1e5 + 1))
t, x, _ = sp.lsim(H, v(t), t)
plot(t, x)
show()

t = linspace(0, 30e-3, int(1e5 + 1))
t, x, _ = sp.lsim(H, v(t), t)
plot(t, x)
show()
