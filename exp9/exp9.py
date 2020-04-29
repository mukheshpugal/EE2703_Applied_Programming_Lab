from pylab import *
from functools import reduce
from scipy.linalg import lstsq
import mpl_toolkits.mplot3d.axes3d as p3

def spectrum(f = None, T = None, N = None, y = None, fmax = None, window = False, display = True, xLim = 4):
	if fmax is None:
		t = linspace(-T, T, N + 1); t = t[:-1]
		dt = t[1] - t[0]
		fmax = 1 / dt
	if y is None:
		if window: n = arange(N)
		y = f(t) * (fftshift(0.54 + 0.46 * cos(2 * pi * n / N)) if window else 1)
	else:
		N = len(y)
	y[0] = 0
	Y = fftshift(fft(fftshift(y))) / float(N)
	if display:
		w = linspace(-pi * fmax, pi * fmax, N + 1); w = w[:-1]
		maxima = reduce(intersect1d, (where(abs(Y) > abs(roll(Y, 1))),\
			where(abs(Y) > abs(roll(Y, -1))), where(abs(Y) > 1e-2)))
		figure()
		subplot(2, 1, 1)
		plot(w, abs(Y), 'b', w[maxima], abs(Y[maxima]), 'bo', lw=2)
		xlim([-xLim, xLim])
		grid(True)
		subplot(2, 1, 2)
		plot(w, angle(Y), 'r.', w[maxima], angle(Y[maxima]), 'go', lw=2)
		xlim([-xLim, xLim])
		show()
	return Y[8:]

spectrum(lambda t : sin(sqrt(2) * t), pi, 64, window = True)
spectrum(lambda t : sin(sqrt(2) * t), 4 * pi, 256, window = True)
spectrum(lambda t : cos(0.86 * t) ** 3, 4 * pi, 256, window = True)
spectrum(lambda t : cos(0.86 * t) ** 3, 4 * pi, 256, window = False)

def estimate(vec):
	N = len(vec)
	vec = fftshift(vec)
	t = linspace(-N * pi / 64,N * pi / 64, N + 1); t = t[:-1]
	dt = t[1] - t[0]
	fmax = 1 / dt
	n = arange(N)
	wnd = fftshift(0.54 + 0.46 * cos(2 * pi * n / N))
	y = vec.copy()
	y[0] = 0
	Y = fftshift(fft(fftshift(y))) / float(N)
	w = linspace(-pi * fmax, pi * fmax, N + 1); w = w[:-1]
	i = intersect1d(where(w>=0), where(abs(Y) > 0.1))
	freq = sum(w[i] * abs(Y[i]**2)) / sum(abs(Y[i]**2))
	A, B = lstsq(c_[cos(freq * t), sin(freq * t)], vec)[0]
	delta = arctan2(-B, A)
	while delta < 0:
		delta += pi
	while delta > pi:
		delat -= pi
	return freq, delta

print(estimate(cos(1.4 * linspace(-2 * pi, 2 * pi, 129)[:-1] + 1.2)))
print(estimate(0.1 * randn(128) + cos(1.3 * linspace(-2 * pi, 2 * pi, 129)[:-1] + 1.2)))

spectrum(lambda t : cos(24 * t + 8 * t * t / pi), pi, 1024, window = False, xLim = 32)

t = linspace(-pi, pi, 1025)[:-1]
dt = t[1] - t[0]
fmax = 1 / dt
w = linspace(0, pi * fmax, 9)[:-1]
Y, X = meshgrid(w, linspace(-pi, pi, 65)[:-1])

surface = array([spectrum(y = cos(24 * x + 8 * x * x / pi), fmax = fmax, display = False) for x in array_split(t, 64)])
ax = p3.Axes3D(figure(4))
surf = ax.plot_surface(Y, X, abs(surface), rstride = 1, cstride = 1, cmap = cm.jet, linewidth = 0, antialiased = True)
show()
