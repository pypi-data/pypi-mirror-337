BPSK Modulation and Demodulation
===============================

This package provides functions for BPSK modulation and demodulation.

Installation
------------

You can install the package via pip:

.. code:: bash

    pip install bpsk_mod

Usage
-----

Here is an example of how to use the package:

```python
import numpy as np
from bpsk_mod.modulation import modulator, demodulator

# Parameters
N = 1000  # Number of bits
L = 16    # Upsampling factor

# Generate random binary message
bit = np.random.randint(0, 2, N)

# Modulate the message
modulated_signal, t = modulator(bit, L)

# Demodulate the signal (e.g., with noise)
received_signal = modulated_signal  # Assume no noise for simplicity
demodulated_bits = demodulator(received_signal, L)

# Print the demodulated bits
print("Demodulated bits:", demodulated_bits)