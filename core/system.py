import configparser
import numpy
import sys
import core.radio.tx.transmitter as tx
import core.radio.rx.receiver as rx
import core.channel.channel as channel


class System():

    def __init__(self):
        self._config = configparser.ConfigParser()
        if 'pytest' in sys.modules:
            self._config.read_dict(self.config_default())
        elif not self._config.read('config.ini'):
            self._config.read_dict(self.config_default())
            self._config_update(
                tx=self.config_default_radio(),
                rx=self.config_default_radio()
            )
            self.config_writefile()
        self._time = None
        self._diagram = None
        self._channel = channel.Channel(self)
        self._radios = {}
        for section, section_value in dict(self._config).items():
            if 'tx' == section[:2]:
                self._radios[section] = tx.Transmitter(self, section)
            elif 'rx' == section[:2]:
                self._radios[section] = rx.Receiver(self, section)

    @property
    def config(self):
        return self._config

    @property
    def channel(self):
        return self._channel

    @property
    def time(self):
        return self._time

    @property
    def radios(self):
        return self._radios

    @property
    def diagram(self):
        return self._diagram

    @diagram.setter
    def diagram(self, value):
        self._diagram = value

    def radio_add(self, radio):
        self._radios[str(radio)] = radio

    def radio_get(self, name):
        self._radios[name]

    def run(self, event=None):
        sim_duration = self._config.getfloat('system', 'sim duration')
        sampling_rate = self._config.getint('system', 'sampling rate')
        self._time = numpy.linspace(0,
            sim_duration,
            int(sampling_rate*sim_duration))
        self._channel.reset()
        for name in sorted(self._radios, reverse=True):
            self._radios[name].process()
        if self._diagram is not None:
            self._diagram.render_afterrun()

    def config_update(self, **kwargs):
        for section, section_value in kwargs.items():
            if not self._config.has_section(section):
                self._config.add_section(section)
            for key, value in section_value.items():
                self._config.set(section, key, value)

    def config_writefile(self):
        file = open('config.ini', 'w')
        self._config.write(file)
        file.close()

    @classmethod
    def config_default(self):
        return {
            'system':
            {
                'sampling rate': '1000000',
                'sim duration' : '1.0'
            },
        }

    @classmethod
    def config_default_radio(self):
        return {
            'carrier frequency': '800',
            'modulation': 'BPSK',
            'start time': '0',
            'symbol duration': '0.005'
        }