from pylab import *

def fft_(f, N, xLim = 15):
	t = linspace(-N * pi / 128, N * pi / 128, N + 1)[:-1]
	y = f(t)
	Y = fftshift(fft(ifftshift(y))) / float(N)
	w = linspace(-64, 64, N + 1)[:-1]
	figure()
	subplot(2, 1, 1)
	plot(w, abs(Y), lw = 2)
	xlim([-xLim, xLim])
	grid(True)
	subplot(2, 1, 2)
	plot(w, angle(Y), lw = 2)
	ii = where(abs(Y) > 1e-3)
	plot(w[ii], angle(Y[ii]), 'ro', lw = 2)
	xlim([-xLim, xLim])
	grid(True)
	show()


fft_(lambda t : sin(5 * t), 128)
fft_(lambda t : (1 + 0.1 * cos(t)) * cos(10 * t), 512)
fft_(lambda t : sin(t) ** 3, 512)
fft_(lambda t : cos(t) ** 3, 512)
fft_(lambda t : cos(20 * t + 5 * cos(t)), 512, xLim = 30)


def estimate(N, T):
	t = linspace(- T / 2, T / 2, N + 1)[:-1]
	w = linspace(- N * pi / T, N * pi / T, N + 1)[:-1]
	y = exp(-0.5 * t**2)
	Y_true = exp(-0.5 * w**2) / sqrt(2 * pi)
	Y = fftshift(fft(ifftshift(y))) * T / (2 * pi * N)

	return sum(abs(Y - Y_true)), w, Y, Y_true

i = 1
while estimate(N = 512, T = i * pi)[0] > 1e-6:
	i += 1

print('Time range for accurate spectrum : ' + str(i) + 'pi')
print('Accuracy : ' + str(estimate(N = 512, T = i * pi)[0]))

w, Y, Y_true = estimate(N = 512, T = i * pi)[1:]

xLim = 5
print(len(Y))
figure()
subplot(2, 1, 1)
plot(w, abs(Y), lw = 2)
xlim([-xLim, xLim])
grid(True)
subplot(2, 1, 2)
plot(w, angle(Y), lw = 2)
ii = where(abs(Y) > 1e-3)
plot(w[ii], angle(Y[ii]), 'ro', lw = 2)
xlim([-xLim, xLim])
grid(True)
show()