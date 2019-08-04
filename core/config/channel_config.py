import numpy
from core.config.system_config import get_system_config

class ChannelConfig():

    def __init__(self):
        system_config = get_system_config()
        self.symbol_duration = 0.1
        self.carrier_freq = 1000



