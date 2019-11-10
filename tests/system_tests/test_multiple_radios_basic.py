import pytest
import numpy


NUM_OF_RADIOS = 2


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


def update_system_config(system, test_configs):
    lengths = []
    for i in range(NUM_OF_RADIOS):
        system.config_update(
            **{
                f'tx{i + 1}': {
                    'modulation': test_configs[i][0],
                    'carrier frequency': test_configs[i][1],
                    'symbol duration': test_configs[i][2],
                },
                f'rx{i + 1}': {
                    'modulation': test_configs[i][0],
                    'carrier frequency': test_configs[i][1],
                    'symbol duration': test_configs[i][2],
                }
            }
        )
        sim_duration = system.config.getfloat('system', 'sim duration')
        length = int(sim_duration/float(test_configs[i][2]))
        if 'BPSK' == test_configs[i][0]:
            multiple = 1
        elif 'QPSK' == test_configs[i][0]:
            multiple = 2
        elif '16QAM' == test_configs[i][0]:
            multiple = 4
        lengths.append((multiple, length*multiple))
    return lengths


@pytest.mark.parametrize('test_configs', testconfig_radios)
def test_full_duration(system, test_configs, init_radios, random_bitstream):
    [tx1, rx1, tx2, rx2] = init_radios(NUM_OF_RADIOS)
    lengths = update_system_config(system, test_configs)
    sizes = [size[1] for size in lengths]
    tx1.bitstream = random_bitstream(sizes[0])
    tx2.bitstream = random_bitstream(sizes[1])
    system.run()
    assert (tx1.bitstream == rx1.bitstream).all()
    assert (tx2.bitstream == rx2.bitstream).all()


@pytest.mark.parametrize('test_configs', testconfig_radios)
def test_partial_duration(system, test_configs, init_radios, random_bitstream):
    [tx1, rx1, tx2, rx2] = init_radios(NUM_OF_RADIOS)
    lengths = update_system_config(system, test_configs)
    lowest = [low[0] for low in lengths]
    highest = [high[1] - high[0] for high in lengths]
    sizes = numpy.random.randint(low=lowest, high=highest)
    tx1.bitstream = random_bitstream(sizes[0])
    tx2.bitstream = random_bitstream(sizes[1])
    system.run()
    assert (tx1.bitstream == rx1.bitstream).all()
    assert (tx2.bitstream == rx2.bitstream).all()


@pytest.mark.parametrize('test_configs', testconfig_radios)
def test_exceed_duration(system, test_configs, init_radios, random_bitstream):
    [tx1, rx1, tx2, rx2] = init_radios(NUM_OF_RADIOS)
    lengths = update_system_config(system, test_configs)
    lowest = [low[0] + low[1] for low in lengths]
    highest = [2*high[1] for high in lengths]
    sizes = numpy.random.randint(low=lowest, high=highest)
    tx1.bitstream = random_bitstream(sizes[0])
    tx2.bitstream = random_bitstream(sizes[1])
    system.run()
    assert (tx1.bitstream[:lengths[0][1]] == rx1.bitstream).all()
    assert (tx2.bitstream[:lengths[1][1]] == rx2.bitstream).all()
