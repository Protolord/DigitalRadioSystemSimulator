import numpy
import core.system as system
import core.radio.tx.iq_mapper as iq_mapper
import core.radio.tx.wave_generator as wave_generator


class Transmitter():

    def __init__(self):
        return None

    @classmethod
    def modulate(modulation_scheme, bitstream):
        return {
            'BPSK' : iq_mapper.bpsk(bitstream),
            'QPSK' : iq_mapper.qpsk(utils.zero_padder(bitstream), 2),
            '16QAM': iq_mapper.qam16(utils.zero_padder(bitstream), 4),
        }[modulation_scheme]

    def process(self, system, bitstream):
        t1 = numpy.where(system.time > self.radio_config.tx_timestart)[0][0]
        t2 = numpy.where(system.time > self.radio_config.tx_timestop)[0][0]
        symbolstream = self.modulate(self.radio_config.tx_modulation, bitstream)
        modulated_signal = wave_generator.qam(system.time[t1:t2], symbolstream,
            self.radio_config.tx_symbol_duration,  self.radio_config.tx_carrier_freq)


