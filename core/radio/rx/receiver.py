import core.system as system
import core.radio.rx.iq_demapper as iq_demapper
import core.radio.rx.wave_detector as wave_detector


class Receiver():

    def __init__(self, system, name):
        self._system = system
        if not self._system.config.has_section(name):
            self._system.config_update(**{name: system.config_default_radio()})
        self._name = name
        self._bitstream = None

    def demodulate(self, symbolstream):
        modulation = self._system.config[self._name]['modulation']
        if 'BPSK' == modulation:
            return iq_demapper.bpsk(symbolstream)
        elif 'QPSK' == modulation:
            return iq_demapper.qpsk(symbolstream)
        elif '16QAM' == modulation:
            return iq_demapper.qam16(symbolstream)
        return None

    @property
    def bitstream(self):
        return self._bitstream

    def __str__(self):
        return self._name

    def process(self):
        symbol_duration = self._system.config.getfloat(self._name, 'symbol duration')
        time_start = self._system.config.getfloat(self._name, 'start time')
        signal = self._system.channel.signal_get(time_start, 1.0)
        symbolstream = wave_detector.qam(self._system.time,
                                         signal,
                                         symbol_duration,
                                         self._system.config.getfloat(self._name, 'carrier frequency'))
        self._bitstream = self.demodulate(symbolstream)


