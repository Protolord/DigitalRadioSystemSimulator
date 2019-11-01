import numpy


def bpsk(symbolstream):
    bitstream = numpy.round((1 - numpy.sqrt(2)*symbolstream.real) / 2)
    return bitstream.astype(numpy.int8)


def qpsk(symbolstream):
    sqrt2 = numpy.sqrt(2)
    bit1 = numpy.round((-sqrt2*symbolstream.real + 1) / 2)
    bit0 = numpy.round((-sqrt2*symbolstream.imag + 1) / 2)
    return numpy.dstack((bit1, bit0)).flatten().astype(numpy.int8)


def qam16(symbolstream):
    sqrt10 = numpy.sqrt(10)
    bit3 = numpy.round((-sqrt10*symbolstream.real + 2) / 4)
    bit2 = numpy.round((-sqrt10*symbolstream.imag + 2) / 4)
    bit1 = numpy.round((sqrt10*numpy.abs(symbolstream.real)) / 4)
    bit0 = numpy.round((sqrt10*numpy.abs(symbolstream.imag)) / 4)
    return numpy.dstack((bit3, bit2, bit1, bit0)).flatten().astype(numpy.int8)
