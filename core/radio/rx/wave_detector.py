import numpy
import core.utils.utils as utils


DETECT_BANDWIDTH_HZ = 10
SYMBOL_VALUE_THRESHOLD = 0.1

def qam(time, signal, symbol_duration, carrier_freq):
    sampling_rate = int(round((time.size - 1)/(time[-1] - time[0])))
    symbolstream_size = int(round(time[-1]/symbol_duration))
    symbolstream = numpy.zeros(symbolstream_size, dtype=complex)
    freq = sampling_rate*numpy.arange(0, int(sampling_rate/2))/sampling_rate
    for i in range(symbolstream_size):
        length = int(time.size/symbolstream_size)
        t1 = i*length
        t2 = (i + 1)*length
        fft = 2*numpy.fft.fft(signal[t1:t2])/length
        f1 = fft.size - int(symbol_duration*utils.find_index(freq, carrier_freq + DETECT_BANDWIDTH_HZ/2))
        f2 = fft.size - int(symbol_duration*utils.find_index(freq, carrier_freq - DETECT_BANDWIDTH_HZ/2))
        symbolstream[i] = utils.max(fft[f1:f2])
        if numpy.abs(symbolstream[i]) <= SYMBOL_VALUE_THRESHOLD:
            return symbolstream[:i]
    return symbolstream