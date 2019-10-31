import pytest
import numpy
import core.system
import core.radio.tx.transmitter as tx
import core.radio.rx.receiver as rx


SAMPLING_RATE = 1000000
SIM_DURATION = 1.0

testconfig_radios = [
    # modulation, carrier frequency, symbol duration
    (( 'BPSK',  '80', '0.2'), ('16QAM', '120', '0.1')),
    (( 'BPSK',  '90', '0.1'), ('16QAM', '130', '0.2')),
    (( 'QPSK', '100', '0.2'), ( 'QPSK', '140', '0.1')),
    (( 'QPSK', '110', '0.1'), ( 'QPSK', '150', '0.2')),
    (('16QAM', '120', '0.2'), ( 'BPSK', '160', '0.1')),
    (('16QAM', '130', '0.1'), ( 'BPSK', '170', '0.2')),
    # extreme symbol duration
    (( 'BPSK', '1000', '0.001'), ( 'QPSK',  '2000', '0.001')),
    (('16QAM', '5000', '0.001'), ( 'BPSK', '10000', '0.001')),
    # # mismatched frequency and symbol duration
    (( 'BPSK',    '8', '0.200'), ( 'QPSK',  '74', '0.321')),
    (('16QAM', '4321', '0.012'), ( 'BPSK', '789', '0.111')),
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

def update_system_config(system, group_configs):
    system.config_update(
        tx1=
        {
            'modulation': group_configs[0][0],
            'carrier frequency': group_configs[0][1],
            'symbol duration': group_configs[0][2],
        },
        rx1=
        {
            'modulation': group_configs[0][0],
            'carrier frequency': group_configs[0][1],
            'symbol duration': group_configs[0][2],
        },
        tx2=
        {
            'modulation': group_configs[1][0],
            'carrier frequency': group_configs[1][1],
            'symbol duration': group_configs[1][2],
        },
        rx2=
        {
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
        lengths.append((length*multiple, multiple))
    return lengths

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
    bitstream_sizes = update_system_config(system, group_configs)
    tx1.bitstream = numpy.random.randint(low=0, high=2, size=bitstream_sizes[0][0], dtype=numpy.int8)
    tx2.bitstream = numpy.random.randint(low=0, high=2, size=bitstream_sizes[1][0], dtype=numpy.int8)
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
    bitstream1_size = numpy.random.randint(low=lengths[0][1], high=lengths[0][0]-lengths[0][1])
    bitstream2_size = numpy.random.randint(low=lengths[1][1], high=lengths[1][0]-lengths[1][1])
    tx1.bitstream = numpy.random.randint(low=0, high=2, size=bitstream1_size, dtype=numpy.int8)
    tx2.bitstream = numpy.random.randint(low=0, high=2, size=bitstream2_size, dtype=numpy.int8)
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
    bitstream1_size = numpy.random.randint(low=lengths[0][0]+lengths[0][1], high=2*lengths[0][0])
    bitstream2_size = numpy.random.randint(low=lengths[1][0]+lengths[1][1], high=2*lengths[1][0])
    tx1.bitstream = numpy.random.randint(low=0, high=2, size=bitstream1_size, dtype=numpy.int8)
    tx2.bitstream = numpy.random.randint(low=0, high=2, size=bitstream2_size, dtype=numpy.int8)
    system.run()
    assert (tx1.bitstream[:lengths[0][0]] == rx1.bitstream).all()
    assert (tx2.bitstream[:lengths[1][0]] == rx2.bitstream).all()