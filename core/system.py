import configparser
import numpy
import core.radio.tx.transmitter as tx
import core.radio.rx.receiver as rx
import core.channel.channel as channel


class System():

    def __init__(self):
        self._config = configparser.ConfigParser()
        if not self._config.read('config.ini'):
            self._config.read_dict(self.default_config())
            self.write_config_file()
        self._channel = channel.Channel(self)
        self._time = None

    @property
    def config(self):
        return self._config

    @property
    def channel(self):
        return self._channel

    @property
    def time(self):
        return self._time

    def update_config(self, **kwargs):
        for section, section_value in kwargs.items():
            for key, value in section_value.items():
                self._config.set(section, key, value)

    def write_config_file(self):
        file = open('config.ini', 'w')
        self._config.write(file)
        file.close()

    def run(self):
        self._time = numpy.linspace(0,
            self._config.getfloat('system', 'sim duration'),
            self._config.getint('system', 'sampling rate'))
        self._channel.reset()


    def default_config(self):
        return {
            'system':
            {
                'sampling rate': 1000000,
                'sim duration' : 1.0
            }
        }