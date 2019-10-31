import numpy
import core.utils.utils as utils


SYMBOL_VALUE_THRESHOLD = 0.1

def qam(time, signal, symbol_duration, carrier_freq):
    sampling_rate = int(time.size//(time[-1] - time[0]))
    symbolstream_size = int((time[-1] - time[0])/symbol_duration)
    symbolstream = numpy.zeros(symbolstream_size, dtype=complex)
    freq = numpy.arange(0, sampling_rate//2)
    rev_per_symbol = carrier_freq*symbol_duration
    length = min(time.size//symbolstream_size, int(time.size*symbol_duration))
    fft_length = int(length*(int(rev_per_symbol)/rev_per_symbol))
    for i in range(symbolstream_size):
        t1 = utils.find_index(time, time[0] + numpy.ceil(i*rev_per_symbol)/carrier_freq)
        t2 = t1 + fft_length
        fft = 2*numpy.fft.fft(signal[t1:t2])/fft_length
        symbolstream[i] = fft[fft.size - int(rev_per_symbol)]
        if numpy.abs(symbolstream[i]) < SYMBOL_VALUE_THRESHOLD:
            return symbolstream[:i]
    return symbolstream