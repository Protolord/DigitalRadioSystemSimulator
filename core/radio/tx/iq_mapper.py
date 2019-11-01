import numpy


# Reference: 3GPP TS 38.211 5.1.2 BPSK
def bpsk(bitstream):
    value = 1 - 2*bitstream
    symbolstream = (value + 1j*value) / numpy.sqrt(2)
    return symbolstream


# Reference: 3GPP TS 38.211 5.1.3 QPSK
def qpsk(bitstream):
    bitgroup = numpy.reshape(bitstream, (-1, 2))
    real = (1 - 2*bitgroup[:, 0])
    imag = (1 - 2*bitgroup[:, 1])
    symbolstream = (real + 1j*imag) / numpy.sqrt(2)
    return symbolstream


# Reference: 3GPP TS 38.211 5.1.4 16QAM
def qam16(bitstream):
    bitgroup = numpy.reshape(bitstream, (-1, 4))
    real = (1 - 2*bitgroup[:, 0]) * (1 + 2*bitgroup[:, 2])
    imag = (1 - 2*bitgroup[:, 1]) * (1 + 2*bitgroup[:, 3])
    symbolstream = (real + 1j*imag) / numpy.sqrt(10)
    return symbolstream
