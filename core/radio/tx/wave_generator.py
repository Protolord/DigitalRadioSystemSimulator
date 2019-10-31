import numpy


def qam(time, symbolstream, symbol_duration, carrier_freq):
    signal = numpy.zeros(time.size)
    angular_freq = 2*numpy.pi*carrier_freq
    length = max(time.size//symbolstream.size, int(time.size*symbol_duration))
    for i, symbol in enumerate(symbolstream):
        t1 = i*length
        t2 = (i + 1)*length
        signal[t1:t2] = (symbol.real*numpy.cos(angular_freq*time[t1:t2]) +
                         symbol.imag*numpy.sin(angular_freq*time[t1:t2]))
    return signal