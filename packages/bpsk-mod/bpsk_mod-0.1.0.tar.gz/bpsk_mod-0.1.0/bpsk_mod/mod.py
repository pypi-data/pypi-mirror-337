import numpy as np

def bpsk_mod(data, fc, of):
    """
    Perform BPSK modulation on input binary data.

    Parameters:
        data (numpy array): Binary data (0s and 1s).
        fc (float): Carrier frequency.
        of (int): Oversampling factor.

    Returns:
        s_t (numpy array): BPSK modulated signal.
    """
    t = np.arange(0, len(data) * of) / of  # Time vector
    data_bpsk = 2 * data - 1  # Convert {0,1} to {-1,1}
    s_t = np.repeat(data_bpsk, of) * np.cos(2 * np.pi * fc * t)
    return s_t