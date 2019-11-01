import pytest
import numpy
import core.system
import core.radio.tx.transmitter as tx
import core.radio.rx.receiver as rx


SAMPLING_RATE = 1000000
SIM_DURATION = 1.0


testconfig_radios = [
    # modulation, carrier frequency, symbol duration
    (('BPSK',    '80', '0.200'), ('16QAM',  '120', '0.100')),
    (('BPSK',    '90', '0.100'), ('16QAM',  '130', '0.200')),
    (('QPSK',   '100', '0.200'), ('QPSK',   '140', '0.100')),
    (('QPSK',   '110', '0.100'), ('QPSK',   '150', '0.200')),
    (('16QAM',  '120', '0.200'), ('BPSK',   '160', '0.100')),
    (('16QAM',  '130', '0.100'), ('BPSK',   '170', '0.200')),
    # extreme symbol duration
    (('BPSK',  '1000', '0.001'), ('QPSK',  '2000', '0.001')),
    (('16QAM', '5000', '0.001'), ('BPSK', '10000', '0.001')),
    # mismatched frequency and symbol duration
    (('BPSK',     '8', '0.200'), ('QPSK',    '74', '0.321')),
    (('16QAM', '4321', '0.012'), ('BPSK',   '789', '0.111')),
]


@pytest.fixture(scope='module')
def system():
    system = core.system.System()
    system.config_update(
        system={
            'sampling rate': str(SAMPLING_RATE),
            'sim duration': str(SIM_DURATION)
        }
    )
    return system


def update_system_config(system, group_configs):
    system.config_update(
        tx1={
            'modulation': group_configs[0][0],
            'carrier frequency': group_configs[0][1],
            'symbol duration': group_configs[0][2],
        },
        rx1={
            'modulation': group_configs[0][0],
            'carrier frequency': group_configs[0][1],
            'symbol duration': group_configs[0][2],
        },
        tx2={
            'modulation': group_configs[1][0],
            'carrier frequency': group_configs[1][1],
            'symbol duration': group_configs[1][2],
        },
        rx2={
            'modulation': group_configs[1][0],
            'carrier frequency': group_configs[1][1],
            'symbol duration': group_configs[1][2],
        }
    )
    lengths = []
    for i in range(2):
        length = int(SIM_DURATION/float(group_configs[i][2]))
        if 'BPSK' == group_configs[i][0]:
            multiple = 1
        elif 'QPSK' == group_configs[i][0]:
            multiple = 2
        elif '16QAM' == group_configs[i][0]:
            multiple = 4
        lengths.append((multiple, length*multiple))
    return lengths


def random_bitstream(size):
    return numpy.random.randint(low=0, high=2, size=size, dtype=numpy.int8)


@pytest.mark.parametrize('group_configs', testconfig_radios)
def test_full_duration(system, group_configs):
    tx1 = tx.Transmitter(system, 'tx1')
    tx2 = tx.Transmitter(system, 'tx2')
    rx1 = rx.Receiver(system, 'rx1')
    rx2 = rx.Receiver(system, 'rx2')
    system.radio_add(rx1)
    system.radio_add(rx2)
    system.radio_add(tx1)
    system.radio_add(tx2)
    lengths = update_system_config(system, group_configs)
    sizes = [size[1] for size in lengths]
    tx1.bitstream = random_bitstream(sizes[0])
    tx2.bitstream = random_bitstream(sizes[1])
    system.run()
    assert (tx1.bitstream == rx1.bitstream).all()
    assert (tx2.bitstream == rx2.bitstream).all()


@pytest.mark.parametrize('group_configs', testconfig_radios)
def test_partial_duration(system, group_configs):
    tx1 = tx.Transmitter(system, 'tx1')
    tx2 = tx.Transmitter(system, 'tx2')
    rx1 = rx.Receiver(system, 'rx1')
    rx2 = rx.Receiver(system, 'rx2')
    system.radio_add(rx1)
    system.radio_add(rx2)
    system.radio_add(tx1)
    system.radio_add(tx2)
    lengths = update_system_config(system, group_configs)
    lowest = [low[0] for low in lengths]
    highest = [high[1] - high[0] for high in lengths]
    sizes = numpy.random.randint(low=lowest, high=highest)
    tx1.bitstream = random_bitstream(sizes[0])
    tx2.bitstream = random_bitstream(sizes[1])
    system.run()
    assert (tx1.bitstream == rx1.bitstream).all()
    assert (tx2.bitstream == rx2.bitstream).all()


@pytest.mark.parametrize('group_configs', testconfig_radios)
def test_exceed_duration(system, group_configs):
    tx1 = tx.Transmitter(system, 'tx1')
    tx2 = tx.Transmitter(system, 'tx2')
    rx1 = rx.Receiver(system, 'rx1')
    rx2 = rx.Receiver(system, 'rx2')
    system.radio_add(rx1)
    system.radio_add(rx2)
    system.radio_add(tx1)
    system.radio_add(tx2)
    lengths = update_system_config(system, group_configs)
    lowest = [low[0] + low[1] for low in lengths]
    highest = [2*high[1] for high in lengths]
    sizes = numpy.random.randint(low=lowest, high=highest)
    tx1.bitstream = random_bitstream(sizes[0])
    tx2.bitstream = random_bitstream(sizes[1])
    system.run()
    assert (tx1.bitstream[:lengths[0][1]] == rx1.bitstream).all()
    assert (tx2.bitstream[:lengths[1][1]] == rx2.bitstream).all()
