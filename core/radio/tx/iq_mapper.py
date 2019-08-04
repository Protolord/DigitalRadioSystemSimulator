import cmath
import numpy
import core.utils.utils as utils

# Reference: TS 38.211 5.1.2 BPSK
def bpsk(bitstream):
    value = (1 - 2*bitstream)
    symbolstream = (value + 1j*value)/cmath.sqrt(2)
    return symbolstream

# Reference: TS 38.211 5.1.3 QPSK
def qpsk(bitstream):
    bitgroup = numpy.reshape(bitstream, (-1, 2))
    real = (1 - 2*bitgroup[:,0])
    imag = (1 - 2*bitgroup[:,1])
    symbolstream = (real + 1j*imag)/cmath.sqrt(2)
    return symbolstream

