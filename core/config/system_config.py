import core.radio.tx.modulator as modulator
import core.radio.tx.wave_generator as wave_generator

class Transmitter():

    def __init__(self):
        self.env_config = EnvironmentConfig()
        self.radio_config = RadioConfig()

    @classmethod
    def modulate(modulation_scheme, bitstring):
        return {
            'bpsk': modulator.bpsk(bitstring),
            'qpsk': modulator.qpsk(bitstring),
        }[modulation_scheme]

    def process(self, bitstring):
        signals = self.modulate(self.radio_config.modulation_scheme, bitstring)
        waveform = wave_generator.process(self.env_config.time, signals, self.env_config.symbol_duration,
                                          self.radio_config.carrier_freq)


