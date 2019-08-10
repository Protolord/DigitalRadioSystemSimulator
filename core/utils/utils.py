import numpy


def max(array):
    max_wave = array[0]
    max_abs = numpy.abs(max_wave)
    for wave in array:
        if numpy.abs(wave) > max_abs:
            max_wave = wave
            max_abs = numpy.abs(wave)
    return max_wave

def isclose(a, b, atol=0, rtol=0.1):
    real = numpy.round(numpy.abs(a.real - b.real), 15) <= atol + rtol*numpy.abs((a.real + b.real)/2)
    imag = numpy.round(numpy.abs(a.imag - b.imag), 15) <= atol + rtol*numpy.abs((a.imag + b.imag)/2)
    return (real & imag)

def zero_padder(bitstream, multiple):
    mod = bitstream.size%multiple
    if 0 == mod:
        return bitstream
    return numpy.pad(bitstream, (0, multiple - mod))
