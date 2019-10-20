import numpy
import core.utils.utils as utils


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
        t1 = utils.find_index(self._system.time, time_start)
        t2 = utils.find_index(self._system.time, time_end) + 1
        return self._signal[t1:t2]

    def signal_add(self, signal, time_start):
        if self._signal is None:
            return
        t1 = utils.find_index(self._system.time, time_start)
        t2 = min(t1 + signal.size, self._system.time.size)
        self._signal[t1:t2] += signal[:t2 - t1]