from numpy import pi, sin, cos
import numpy as np

def sine_wave(t, fre, n):
    """
    Return a basic sine wave
    n does not matter here

    Parameters
    ----------
    t : array-like
        Time array. Here will be passed time 0 to 2P, where P is the period
    fre : int or float
        Frequency in Hz of the wave
    n : int
        Number of terms in the Fourier Series

    Returns
    -------
    f : array-like
        Resulting function applied along t
    freqs : array-like
        Frequency array of each term in the series
    amps : array-like
        Amplitude array of each term in the series
    """
    f = sin(2*pi*fre*t)
    freqs = np.array([fre])
    amps = np.array([1])
    return f, freqs, amps

def square_wave(t, fre, n=15):
    """
    Square wave composed of n sine waves
    Same parameters as the sine_wave method
    """
    f = np.zeros(t.shape[0])
    freqs = np.array([])
    amps = np.array([])
    n = int(n)
    for i in xrange(1, n+1):
        f += (4 / pi) * (1.0 / (2*i-1)) * sin((2*i-1)*2*pi*fre*t)
        freqs = np.append(freqs, fre*(2*i-1))
        amps = np.append(amps, (2 / pi) * (1.0 / (2*i-1)))
    return f, freqs, amps

def triangle_wave(t, fre, n=15):
    """
    Triangle wave composed of n sine waves
    Same parameters as the sine_wave method
    """
    f = np.zeros(t.shape[0])
    n = int(n)
    freqs = np.array([])
    amps = np.array([])
    for i in xrange(1, n+1):
        f -= (8 / pi**2) * (1.0 / (2*i-1)**2) * cos((2*i-1)*2*pi*fre*t)
        freqs = np.append(freqs, fre*(2*i-1))
        amps = np.append(amps, (4 / (pi*(2*i-1))**2))
    return f, freqs, amps

def sawtooth_wave(t, fre, n=15):
    """
    Sawtooth wave composed of n sine waves
    Same parameters as the sine_wave method
    """
    f = np.zeros(t.shape[0])
    n = int(n)
    freqs = np.array([])
    amps = np.array([])
    for i in xrange(1, n+1):
        f += (2 / pi) * (1.0 / i) * sin(i*2*pi*fre*t)
        freqs = np.append(freqs, fre*i)
        amps = np.append(amps, 1 / (pi * i))
    return f, freqs, amps

def half_rectified_sine(t, fre, n=15):
    """
    Half rectified sine wave composed of n sine waves
    Same parameters as the sine_wave method
    """
    f = 1/pi + sin(2*pi*fre*t)/2
    n = int(n)
    freqs = np.array([fre])
    amps = np.array([0.5])
    if n < 2:
        return f, freqs, amps
    else:
        for i in xrange(1, n):
            f -= (2 / pi) * cos(i*4*pi*fre*t) / (4*i**2-1)
            freqs = np.append(freqs, fre*i*2)
            amps = np.append(amps, 2 / (pi*(4*i**2-1)))
        return f, freqs, amps

def full_rectified_sine(t, fre, n=15):
    """
    Full rectified sine wave composed of n sine waves
    Same parameters as the sine_wave method
    """
    f = np.ones(t.shape[0]) * 2/pi
    n = int(n)
    freqs = np.array([0])
    amps = np.array([2/pi])
    for i in xrange(1, n):
        f -= (4 / pi) * cos(i*2*pi*fre*t) / (4*i**2-1)
        freqs = np.append(freqs, fre*i)
        amps = np.append(amps, 4 / (pi*(4*i**2-1)))
    return f, freqs, amps
