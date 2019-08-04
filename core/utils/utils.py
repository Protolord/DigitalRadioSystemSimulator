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
    # if a.size != b.size:
    print('Unmatching size: a.size=' + str(a.size) + ', b.size=' + str(b.size))
    table = numpy.abs(numpy.abs(a) - numpy.abs(b)) <= atol + rtol*numpy.abs(b)
    return table

def zero_padder(bitstream, multiple):
    count = bitstream.size%multiple
    if 0 == count:
        return bitstream
    return numpy.pad(bitstream, (0, count))
