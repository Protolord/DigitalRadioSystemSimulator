import cmath
import math
import numpy
import core.utils.plotter as plotter
import core.utils.utils as utils


def qam(time, signal, symbol_duration, carrier_freq):
    bandwidth = 20
    sampling_rate = int(round((time.size - 1)/(time[-1] - time[0])))
    symbolstream_size = int(round(time[-1]/symbol_duration))
    symbolstream = numpy.zeros(symbolstream_size, dtype=complex)
    freq = sampling_rate*numpy.arange(0, int(sampling_rate/2))/sampling_rate
    print()
    for i in range(symbolstream_size):
        length = int(time.size/symbolstream_size)
        t1 = i*length
        t2 = (i + 1)*length
        fft = 2*numpy.fft.fft(signal[t1:t2])/length
        f1 = fft.size - int(symbol_duration*numpy.where(freq > carrier_freq + bandwidth/2)[0][0])
        f2 = fft.size - int(symbol_duration*numpy.where(freq > carrier_freq - bandwidth/2)[0][0])
        if i == 0:
            plotter.vertical_line(f1, 'red')
            plotter.vertical_line(f2, 'blue')
            plotter.fft(signal[t1:t2], length)
            plotter.time_domain(time[t1:t2], signal[t1:t2])
        symbolstream[i] = utils.max(fft[f1:f2])
    return symbolstream