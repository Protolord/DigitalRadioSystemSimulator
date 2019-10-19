import pytest
import numpy
import core.system
import core.radio.tx.transmitter as tx
import core.radio.rx.receiver as rx


SAMPLING_RATE = 10000
SIM_DURATION = 1.0
TEST_REPEAT = 5

@pytest.fixture(scope='module')
def system():
    system = core.system.System()
    system.config_update(
        system=
        {
            'sampling rate': str(SAMPLING_RATE),
            'sim duration' : str(SIM_DURATION)
        }
    )
    return system

def test_single_radio_full_duration(system):
    tx1 = tx.Transmitter(system, 'tx1')
    rx1 = rx.Receiver(system, 'rx1')
    system.radio_add(rx1)
    system.radio_add(tx1)
    for _ in range(TEST_REPEAT):
        tx1.bitstream = numpy.random.randint(low=0, high=2, size=10, dtype=numpy.int8)
        system.run()
        assert (tx1.bitstream == rx1.bitstream).all()

def test_single_radio_partial_duration(system):
    tx1 = tx.Transmitter(system, 'tx1')
    rx1 = rx.Receiver(system, 'rx1')
    system.radio_add(rx1)
    system.radio_add(tx1)
    for _ in range(TEST_REPEAT):
        bitstream_size = numpy.random.randint(low=1, high=9)
        tx1.bitstream = numpy.random.randint(low=0, high=2, size=bitstream_size, dtype=numpy.int8)
        system.run()
        assert (tx1.bitstream == rx1.bitstream).all()

def test_multiple_radio_full_duration(system):
    tx1 = tx.Transmitter(system, 'tx1')
    tx2 = tx.Transmitter(system, 'tx2')
    rx1 = rx.Receiver(system, 'rx1')
    rx2 = rx.Receiver(system, 'rx2')
    system.radio_add(rx1)
    system.radio_add(rx2)
    system.radio_add(tx1)
    system.radio_add(tx2)
    system.config_update(
        tx1=
        {
            'carrier frequency': '50',
            'symbol duration': '0.2',
            'modulation': 'BPSK',
        },
        rx1=
        {
            'carrier frequency': '50',
            'symbol duration': '0.2',
            'modulation': 'BPSK',
        },
        tx2=
        {
            'carrier frequency': '100',
            'symbol duration': '0.1',
            'modulation': 'QPSK',
        },
        rx2=
        {
            'carrier frequency': '100',
            'symbol duration': '0.1',
            'modulation': 'QPSK',
        }
    )
    for _ in range(TEST_REPEAT):
        tx1.bitstream = numpy.random.randint(low=0, high=2, size=5, dtype=numpy.int8)
        tx2.bitstream = numpy.random.randint(low=0, high=2, size=20, dtype=numpy.int8)
        system.run()
        assert (tx1.bitstream == rx1.bitstream).all()
        assert (tx2.bitstream == rx2.bitstream).all()

def test_multiple_radio_partial_duration(system):
    tx1 = tx.Transmitter(system, 'tx1')
    tx2 = tx.Transmitter(system, 'tx2')
    rx1 = rx.Receiver(system, 'rx1')
    rx2 = rx.Receiver(system, 'rx2')
    system.radio_add(rx1)
    system.radio_add(rx2)
    system.radio_add(tx1)
    system.radio_add(tx2)
    system.config_update(
        tx1=
        {
            'carrier frequency': '50',
            'symbol duration': '0.1',
            'modulation': 'QPSK',
        },
        rx1=
        {
            'carrier frequency': '50',
            'symbol duration': '0.1',
            'modulation': 'QPSK',
        },
        tx2=
        {
            'carrier frequency': '100',
            'symbol duration': '0.1',
            'modulation': '16QAM',
        },
        rx2=
        {
            'carrier frequency': '100',
            'symbol duration': '0.1',
            'modulation': '16QAM',
        }
    )
    for _ in range(TEST_REPEAT):
        bitstream1_size = numpy.random.randint(low=1, high=9)
        bitstream2_size = numpy.random.randint(low=1, high=39)
        tx1.bitstream = numpy.random.randint(low=0, high=2, size=bitstream1_size, dtype=numpy.int8)
        tx2.bitstream = numpy.random.randint(low=0, high=2, size=bitstream2_size, dtype=numpy.int8)
        system.run()
        assert (tx1.bitstream == rx1.bitstream).all()
        assert (tx2.bitstream == rx2.bitstream).all()