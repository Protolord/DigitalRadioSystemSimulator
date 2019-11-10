import pytest
import numpy
import core.system
import core.radio.tx.transmitter as transmitter
import core.radio.rx.receiver as receiver


SAMPLING_RATE = 1000000
SIM_DURATION = 1.0


@pytest.fixture(scope='session')
def random_bitstream():
    def func(size):
        return numpy.random.randint(low=0, high=2, size=size, dtype=numpy.int8)
    return func


@pytest.fixture(scope='session')
def system():
    system = core.system.System()
    system.config_update(
        system={
            'sampling rate': str(SAMPLING_RATE),
            'sim duration': str(SIM_DURATION)
        }
    )
    return system


@pytest.fixture(scope='session')
def init_radios(system):
    def func(num_of_radios):
        system._radios = {}
        res = []
        for i in range(num_of_radios):
            tx = transmitter.Transmitter(system, f'tx{i + 1}')
            rx = receiver.Receiver(system, f'rx{i + 1}')
            system.radio_add(tx)
            system.radio_add(rx)
            res.extend([tx, rx])
        return res
    return func
