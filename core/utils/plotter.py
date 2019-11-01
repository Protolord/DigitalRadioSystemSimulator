import numpy
import matplotlib.pyplot as pyplot


def time_domain(time, signal):
    pyplot.plot(time, signal)
    pyplot.show()


def freq_domain(time, signal):
    sampling_rate = int(round((time.size) / (time[-1]-time[0])))
    freq = numpy.linspace(0, sampling_rate//2, time.size//2)
    fft_data = 2*numpy.fft.fft(signal)/time.size
    pyplot.plot(freq, numpy.abs(fft_data[:time.size//2]))
    pyplot.show()


def symbol(sym):
    x = numpy.linspace(-1, 1, 1000)
    y = numpy.sqrt(1 - x*x)
    pyplot.plot(x, y, color='red')
    pyplot.plot(x, -y, color='red')
    pyplot.plot([0, sym.real], [0, sym.imag], '-')
    pyplot.show()


def freq_domain_mirror(time, signal):
    sampling_rate = int(round((time.size - 1) / (time[-1]-time[0])))
    freq = numpy.linspace(0, sampling_rate//2, time.size//2)
    fft_data = 2*numpy.fft.fft(signal)/time.size
    pyplot.plot(freq, numpy.abs(fft_data[int(time.size/2):time.size]))
    pyplot.show()


def fft(signal, length):
    fft_data = 2*numpy.fft.fft(signal)/length
    pyplot.plot(numpy.abs(fft_data))
    pyplot.show()


def vertical_line(x_value, color_value='blue'):
    pyplot.axvline(x=x_value, color=color_value)
