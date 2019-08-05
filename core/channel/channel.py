import numpy
import core.config.channel_config as config


class Channel():

    def __init__(self):
        self.config = config.ChannelConfig()

    def get_signal(self):
        x = 0
        return x