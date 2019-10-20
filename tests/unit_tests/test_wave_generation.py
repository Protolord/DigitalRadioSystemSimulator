import pytest
import numpy
import core.radio.tx.wave_generator as wave_generator
import core.utils.utils as utils


def test_qam():
    time = numpy.linspace(0, 1, int(1e5))
    carrier_freq = 400
    angular_freq = 2*numpy.pi*carrier_freq
    symbol_duration = 0.25
    expected_waveform_cos1 =  1*numpy.cos(angular_freq*time[0:25000])
    expected_waveform_sin1 =  2*numpy.sin(angular_freq*time[0:25000])
    expected_waveform_cos2 =  3*numpy.cos(angular_freq*time[25000:50000])
    expected_waveform_sin2 = -4*numpy.sin(angular_freq*time[25000:50000])
    expected_waveform_cos3 = -5*numpy.cos(angular_freq*time[50000:75000])
    expected_waveform_sin3 =  6*numpy.sin(angular_freq*time[50000:75000])
    expected_waveform_cos4 = -7*numpy.cos(angular_freq*time[75000:100000])
    expected_waveform_sin4 = -8*numpy.sin(angular_freq*time[75000:100000])
    expected_waveform = numpy.stack([expected_waveform_cos1 + expected_waveform_sin1,
                                     expected_waveform_cos2 + expected_waveform_sin2,
                                     expected_waveform_cos3 + expected_waveform_sin3,
                                     expected_waveform_cos4 + expected_waveform_sin4]).flatten()
    actual_symbolstream = numpy.array([1 + 2j, 3 - 4j, -5 + 6j, -7 - 8j])
    actual_waveform = wave_generator.qam(time, actual_symbolstream, symbol_duration, carrier_freq)
    assert (utils.isclose(expected_waveform, actual_waveform, atol=0.1, rtol=0.05)).all()