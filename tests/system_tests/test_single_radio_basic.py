import pytest
import numpy


NUM_OF_RADIOS = 1


testconfig_radios = [
    # modulation, carrier frequency, symbol duration
    ('BPSK',    '80', '0.200'),
    ('BPSK',    '90', '0.100'),
    ('QPSK',   '100', '0.200'),
    ('QPSK',   '110', '0.100'),
    ('16QAM',  '120', '0.200'),
    ('16QAM',  '130', '0.100'),
    # extreme symbol duration
    ('BPSK',  '1000', '0.001'),
    ('QPSK',  '2000', '0.001'),
    ('16QAM', '3000', '0.001'),
    # mismatched frequency and symbol duration
    ('BPSK',     '8', '0.200'),
    ('BPSK',    '10', '0.250'),
    ('QPSK',   '123', '0.120'),
    ('16QAM', '1234', '0.123'),
]


def update_system_config(system, test_configs):
    system.config_update(
        tx1={
            'modulation': test_configs[0],
            'carrier frequency': test_configs[1],
            'symbol duration': test_configs[2],
        },
        rx1={
            'modulation': test_configs[0],
            'carrier frequency': test_configs[1],
            'symbol duration': test_configs[2],
        }
    )
    sim_duration = system.config.getfloat('system', 'sim duration')
    length = int(sim_duration/float(test_configs[2]))
    if 'BPSK' == test_configs[0]:
        multiple = 1
    elif 'QPSK' == test_configs[0]:
        multiple = 2
    elif '16QAM' == test_configs[0]:
        multiple = 4
    return (multiple, length*multiple)


@pytest.mark.parametrize('test_configs', testconfig_radios)
def test_full_duration(system, test_configs, init_radios, random_bitstream):
    [tx1, rx1] = init_radios(NUM_OF_RADIOS)
    size = update_system_config(system, test_configs)[1]
    tx1.bitstream = random_bitstream(size)
    system.run()
    assert (tx1.bitstream == rx1.bitstream).all()


@pytest.mark.parametrize('test_configs', testconfig_radios)
def test_partial_duration(system, test_configs, init_radios, random_bitstream):
    [tx1, rx1] = init_radios(NUM_OF_RADIOS)
    length = update_system_config(system, test_configs)
    size = numpy.random.randint(low=length[0], high=length[1]-length[0])
    tx1.bitstream = random_bitstream(size)
    system.run()
    assert (tx1.bitstream == rx1.bitstream).all()


@pytest.mark.parametrize('test_configs', testconfig_radios)
def test_exceed_duration(system, test_configs, init_radios, random_bitstream):
    [tx1, rx1] = init_radios(NUM_OF_RADIOS)
    length = update_system_config(system, test_configs)
    size = numpy.random.randint(low=length[1], high=2*length[1])
    tx1.bitstream = random_bitstream(size)
    system.run()
    assert (tx1.bitstream[:length[1]] == rx1.bitstream).all()
