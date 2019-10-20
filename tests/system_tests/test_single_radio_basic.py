import pytest
import numpy
import core.system
import core.radio.tx.transmitter as tx
import core.radio.rx.receiver as rx


SAMPLING_RATE = 100000
SIM_DURATION = 1.0

testconfig_radio = [
    # modulation, carrier frequency, symbol duration
    ( 'BPSK',  '80', '0.2'),
    ( 'BPSK',  '90', '0.1'),
    ( 'QPSK', '100', '0.2'),
    ( 'QPSK', '110', '0.1'),
    ('16QAM', '120', '0.2'),
    ('16QAM', '130', '0.1'),
]

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

def update_system_config(system, configs):
    system.config_update(
        tx1=
        {
            'modulation': configs[0],
            'carrier frequency': configs[1],
            'symbol duration': configs[2],
        },
        rx1=
        {
            'modulation': configs[0],
            'carrier frequency': configs[1],
            'symbol duration': configs[2],
        }
    )
    length = int(SIM_DURATION/float(configs[2]))
    if 'QPSK' == configs[0]:
        length *= 2
    elif '16QAM' == configs[0]:
        length *= 4
    return length

@pytest.mark.parametrize('configs', testconfig_radio)
def test_full_duration(system, configs):
    tx1 = tx.Transmitter(system, 'tx1')
    rx1 = rx.Receiver(system, 'rx1')
    system.radio_add(rx1)
    system.radio_add(tx1)
    bitstream_size = update_system_config(system, configs)
    tx1.bitstream = numpy.random.randint(low=0, high=2, size=bitstream_size, dtype=numpy.int8)
    system.run()
    assert (tx1.bitstream == rx1.bitstream).all()

@pytest.mark.parametrize('configs', testconfig_radio)
def test_partial_duration(system, configs):
    tx1 = tx.Transmitter(system, 'tx1')
    rx1 = rx.Receiver(system, 'rx1')
    system.radio_add(rx1)
    system.radio_add(tx1)
    length = update_system_config(system, configs)
    bitstream_size = numpy.random.randint(low=1, high=length-1)
    tx1.bitstream = numpy.random.randint(low=0, high=2, size=bitstream_size, dtype=numpy.int8)
    system.run()
    assert (tx1.bitstream == rx1.bitstream).all()

@pytest.mark.parametrize('configs', testconfig_radio)
def test_exceed_duration(system, configs):
    tx1 = tx.Transmitter(system, 'tx1')
    rx1 = rx.Receiver(system, 'rx1')
    system.radio_add(rx1)
    system.radio_add(tx1)
    length = update_system_config(system, configs)
    bitstream_size = numpy.random.randint(low=length+1, high=2*length)
    tx1.bitstream = numpy.random.randint(low=0, high=2, size=bitstream_size, dtype=numpy.int8)
    system.run()
    assert (tx1.bitstream[:length] == rx1.bitstream).all()