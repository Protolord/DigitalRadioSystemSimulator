import sys
import configparser
import numpy
import core.radio.tx.transmitter as transmitter
import core.radio.rx.receiver as receiver
import core.channel.channel as channel


class System():

    def __init__(self):
        self._config = configparser.ConfigParser()
        if 'pytest' in sys.modules:
            self._config.read_dict(self.config_default())
        elif not self._config.read('config.ini'):
            self._config.read_dict(self.config_default())
            self.config_update(
                tx=self.config_default_radio(),
                rx=self.config_default_radio()
            )
            self.config_writefile()
        self._running = False
        self._time = None
        self._bar = None
        self._thread_lock = None
        self._channel = channel.Channel(self)
        self._radios = {}
        for section in dict(self._config).keys():
            if section.startswith('tx'):
                self._radios[section] = transmitter.Transmitter(self, section)
            elif section.startswith('rx'):
                self._radios[section] = receiver.Receiver(self, section)

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
    def running(self):
        if self._thread_lock is None:
            return self._running
        else:
            with self._thread_lock:
                return self._running

    @running.setter
    def running(self, value):
        if self._thread_lock is None:
            self._running = value
        else:
            with self._thread_lock:
                self._running = value
            if not value:
                self._thread_lock = None
                self._bar = None

    def radio_add(self, radio):
        self._radios[str(radio)] = radio

    def radio_get(self, name):
        return self._radios[name]

    def update_bar(self, status, value):
        if self._bar is not None:
            self._bar.update(status, value)

    def run(self, bar=None, lock=None):
        self._bar = bar
        self._thread_lock = lock
        self.running = True
        sim_duration = self._config.getfloat('system', 'sim duration')
        sampling_rate = self._config.getint('system', 'sampling rate')
        self._time = numpy.linspace(
            0, sim_duration, int(sampling_rate*sim_duration)
        )
        self._channel.reset()
        tx_list = [key for key in self._radios if 'tx' in key]
        rx_list = [key for key in self._radios if 'rx' in key]
        for i, tx in enumerate(tx_list):
            if not self.running:
                return
            self.update_bar(f'Processing {tx}', 50*i/len(tx_list))
            self._radios[tx].process()
        for i, rx in enumerate(rx_list):
            if not self.running:
                break
            self.update_bar(f'Processing {rx}', 50*i/len(rx_list) + 50)
            self._radios[rx].process()
        if not self.running:
            for rx in rx_list:
                self._radios[rx].reset()
            return
        self.update_bar('Simulation Complete', 100)
        self.running = False

    def run_stop(self):
        self.running = False

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
    def config_default(cls):
        return {
            'system':
            {
                'sampling rate': '1000000',
                'sim duration': '1.0'
            },
        }

    @classmethod
    def config_default_radio(cls):
        return {
            'carrier frequency': '800',
            'modulation': 'BPSK',
            'start time': '0',
            'symbol duration': '0.005'
        }
