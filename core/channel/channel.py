import numpy


class Channel():

    def __init__(self, system):
        self._system = system
        self._signal = None

    @property
    def time(self):
        return self._system.time

    def reset(self):
        if self._system.time is None:
            return
        self._signal = numpy.zeros(self._system.time.size)

    def signal_get(self, time_start, time_end):
        if self._signal is None:
            return
        t1 = int(numpy.where(self._system.time >= time_start)[0][0])
        t2 = int(numpy.where(self._system.time >= time_end)[0][0]) + 1
        return self._signal[t1:t2]

    def signal_add(self, signal, time_start):
        if self._signal is None:
            return
        t1 = int(numpy.where(self._system.time >= time_start)[0][0])
        t2 = t1 + signal.size
        if t2 > self._system.time.size:
            t2 = self._system.time.size
        self._signal[t1:t2] += signal[:t2 - t1]