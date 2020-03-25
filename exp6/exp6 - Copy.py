from pylab import *
import scipy.signal as sp

# Transfer function of two port network
H = sp.lti([1], [1e-4, 1])
w, S, phi = H.bode()
subplot(2, 1, 1)
semilogx(w, S)
subplot(2, 1, 2)
semilogx(w, phi)
show()