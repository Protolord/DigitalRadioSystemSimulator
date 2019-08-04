import numpy

def bpsk(symbolstream):
    bitstream = (numpy.round((1 - symbolstream.real*numpy.sqrt(2))/2) > 0)
    return bitstream

def qpsk(symbolstream):
    bit0 = (-numpy.sqrt(2)*symbolstream.real + 1)/2
    bit1 = (-numpy.sqrt(2)*symbolstream.imag + 1)/2
    return numpy.dstack((bit0, bit1)).flatten()
