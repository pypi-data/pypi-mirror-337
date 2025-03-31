import numpy as np
from scipy.signal import upfirdn

def modulator(ak, L):
    """
    Modulate the input binary sequence using BPSK modulation.
    
    Parameters:
    - ak (numpy array): Binary sequence to be modulated (0s and 1s).
    - L (int): Upsampling factor.
    
    Returns:
    - numpy array: Modulated BPSK signal
    - numpy array: Time vector
    """
    # BPSK modulation: map bits (0, 1) to symbols (-1, 1)
    a_bb = upfirdn(h=[1]*L, x=2*ak-1, up=L)  # Upsampling and modulation
    t = np.arange(0, len(ak) * L)  # Time vector for plotting
    return a_bb, t


def demodulator(r_bb, L):
    """
    Demodulate the BPSK signal.
    
    Parameters:
    - r_bb (numpy array): Received BPSK signal after noise addition.
    - L (int): Upsampling factor.
    
    Returns:
    - numpy array: Demodulated binary sequence
    """
    # Extract the real part of the received signal
    x = np.real(r_bb)
    x = np.convolve(x, np.ones(L), mode='same')  # Matched filtering
    ak_hat = (x > 0).astype(int)  # BPSK demodulation (thresholding)
    return ak_hat