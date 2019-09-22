import numpy
import core.config.system_config as config
import core.radio.tx.transmitter as tx
import core.radio.rx.receiver as rx
import core.channel.channel as channel


class System():

    def __init__(self):
        self.config = config.SystemConfig()
        self.channel = channel.Channel()
        self.radios = [(tx.Transmitter(), rx.Receiver())]
        self.time = numpy.linspace(0, self.config.sim_duration, int(self.config.sim_duration*self.config.sampling_rate))