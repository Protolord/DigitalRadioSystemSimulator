import cmath
import numpy
import matplotlib.pyplot as pyplot


def qam(time, symbolstream, symbol_duration, carrier_freq):
    signal = numpy.zeros(time.size)
    for i, symbol in enumerate(symbolstream):
        length = time.size*symbol_duration
        t1 = int(i*length)
        t2 = int((i + 1)*length)
        hyp = numpy.abs(symbol)
        phase = cmath.phase(symbol)
        angular_freq = 2*numpy.pi*carrier_freq
        signal[t1:t2] = hyp*numpy.cos(phase)*numpy.cos(angular_freq*time[t1:t2])
        signal[t1:t2] += hyp*numpy.sin(phase)*numpy.sin(angular_freq*time[t1:t2])
    return signal