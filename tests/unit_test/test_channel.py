import pytest
import numpy
import core.system
import core.utils.plotter as plotter


# SAMPLING_RATE*SIM_DURATION is assumed to be divisible by four
SAMPLING_RATE = 10000
SIM_DURATION = 1.0
TIME_STEP = SIM_DURATION/(SAMPLING_RATE - 1)

@pytest.fixture(scope='module')
def channel():
    system = core.system.System()
    system.update_config(
        system=
        {
            'sampling rate': str(SAMPLING_RATE),
            'sim duration' : str(SIM_DURATION)
        }
    )
    system.run()
    return system.channel

@pytest.fixture(scope='function', autouse=True)
def reset_channel(channel):
    channel.reset()

def test_fulltime_single_add(channel):
    signal = numpy.sin(2*numpy.pi*100*channel.time)
    channel.signal_add(signal, 0)
    assert (signal == channel.signal_get(0, SIM_DURATION)).all()

def test_fulltime_multiple_add(channel):
    signal1 = numpy.sin(2*numpy.pi*100*channel.time)
    signal2 = numpy.cos(2*numpy.pi*100*channel.time)
    signal3 = numpy.linspace(0, 5, channel.time.size)
    channel.signal_add(signal1, 0)
    channel.signal_add(signal2, 0)
    channel.signal_add(signal3, 0)
    assert (signal1 + signal2 + signal3 == channel.signal_get(0, SIM_DURATION)).all()

def test_parttime_single_add(channel):
    signal = numpy.sin(2*numpy.pi*100*channel.time)
    channel.signal_add(signal, SIM_DURATION/2)
    index_half = channel.time.size//2
    assert (numpy.zeros(index_half) == channel.signal_get(0, SIM_DURATION/2 - TIME_STEP)).all()
    assert (signal[:index_half] == channel.signal_get(SIM_DURATION/2, SIM_DURATION)).all()

def test_parttime_multiple_add(channel):
    signal1 = numpy.sin(2*numpy.pi*100*channel.time)
    signal2 = numpy.cos(2*numpy.pi*100*channel.time)
    signal3 = numpy.linspace(0, 5, channel.time.size)
    channel.signal_add(signal1, SIM_DURATION/4)
    channel.signal_add(signal2, 2*SIM_DURATION/4)
    channel.signal_add(signal3, 3*SIM_DURATION/4)
    index_quarter = channel.time.size//4
    quarter_1st = slice(0, index_quarter)
    quarter_2nd = slice(index_quarter, 2*index_quarter)
    quarter_3rd = slice(2*index_quarter, 3*index_quarter)
    assert (numpy.zeros(index_quarter) ==
            channel.signal_get(0, SIM_DURATION/4 - TIME_STEP)).all()
    assert (signal1[quarter_1st] ==
            channel.signal_get(SIM_DURATION/4, 2*SIM_DURATION/4 - TIME_STEP)).all()
    assert (signal1[quarter_2nd] + signal2[quarter_1st] ==
            channel.signal_get(2*SIM_DURATION/4, 3*SIM_DURATION/4 - TIME_STEP)).all()
    assert (signal1[quarter_3rd] + signal2[quarter_2nd] + signal3[quarter_1st] ==
            channel.signal_get(3*SIM_DURATION/4, SIM_DURATION)).all()
