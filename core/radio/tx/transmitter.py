import numpy
import core.system as system
import core.radio.tx.iq_mapper as iq_mapper
import core.radio.tx.wave_generator as wave_generator
import core.utils.utils as utils


class Transmitter():

    def __init__(self, system, name):
        self._system = system
        if not self._system.config.has_section(name):
            self._system.config_update(**{name: system.config_default_radio()})
        self._name = name
        self._bitstream = None

    def modulate(self):
        modulation = self._system.config[self._name]['modulation']
        if 'BPSK' == modulation:
            return iq_mapper.bpsk(self._bitstream)
        elif 'QPSK' == modulation:
            self._bitstream = utils.zero_padder(self._bitstream, 2)
            return iq_mapper.qpsk(self._bitstream)
        elif '16QAM' == modulation:
            self._bitstream = utils.zero_padder(self._bitstream, 4)
            return iq_mapper.qam16(self._bitstream)
        return None

    @property
    def name(self):
        return self._name

    @property
    def bitstream(self):
        return self._bitstream

    @bitstream.setter
    def bitstream(self, value):
        self._bitstream = value

    def process(self):
        symbol_duration = self._system.config.getfloat(self._name, 'symbol duration')
        symbolstream = self.modulate()
        time_start = self._system.config.getfloat(self._name, 'start time')
        time_end = time_start + symbolstream.size*symbol_duration
        t1 = utils.find_index(self._system.time, time_start)
        t2 = utils.find_index(self._system.time, time_end) + 1
        signal = wave_generator.qam(self._system.time[t1:t2],
                                    symbolstream,
                                    self._system.config.getfloat(self._name, 'carrier frequency'))
        self._system.channel.signal_add(signal, time_start)


