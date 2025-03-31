import numpy as np

def bpsk_demod(received_signal, fc, of):
    """
    Perform BPSK demodulation on the received signal.

    Parameters:
        received_signal (numpy array): Noisy received signal.
        fc (float): Carrier frequency.
        of (int): Oversampling factor.

    Returns:
        data_hat (numpy array): Demodulated binary data.
    """
    t = np.arange(0, len(received_signal)) / of  # Time vector
    coherent = received_signal * np.cos(2 * np.pi * fc * t)  # Coherent detection
    data_hat = (np.mean(coherent.reshape(-1, of), axis=1) > 0).astype(int)
    return data_hat