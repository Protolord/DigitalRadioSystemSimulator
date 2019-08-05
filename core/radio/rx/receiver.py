import core.system as system
import core.config.radio_config as config
import core.radio.rx.iq_demapper as iq_demapper
import core.radio.rx.wave_detector as wave_detector


class Receiver():

    def __init__(self):
        self.radio_config = config.RadioConfig()

    @classmethod
    def demodulate(modulation_scheme, symbolstream):
        return {
            'BPSK' : iq_demapper.bpsk(symbolstream),
            'QPSK' : iq_demapper.qpsk(symbolstream),
            '16QAM': iq_demapper.qam16(symbolstream),
        }[modulation_scheme]

    def process(self, system):
        signal = system.channel.get_signal()



