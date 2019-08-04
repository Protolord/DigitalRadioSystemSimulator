import numpy
from core.config.system_config import get_system_config

class RadioConfig():

    def __init__(self):
        system_config = get_system_config()
        self.symbol_duration = 0.1
        self.carrier_freq = 1000
        # total_size = system_config.total_time*system_config.sample_size
        # self.tx_time = numpy.linspace(0, system_config.total_time, total_size)


