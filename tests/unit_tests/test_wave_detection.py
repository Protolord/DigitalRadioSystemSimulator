import pytest
import numpy
import core.radio.rx.wave_detector as wave_detector
import core.utils.utils as utils


def test_qam():
    time = numpy.linspace(0, 1, int(1e5))
    symbol_duration = 0.25
    carrier_freq = 400
    angular_freq = 2*numpy.pi*carrier_freq
    expected_symbolstream = numpy.array([-1 - 2j, -3 + 4j, 5 - 6j, 7 + 8j])
    actual_waveform_cos1 = -1*numpy.cos(angular_freq*time[0:25000])
    actual_waveform_sin1 = -2*numpy.sin(angular_freq*time[0:25000])
    actual_waveform_cos2 = -3*numpy.cos(angular_freq*time[25000:50000])
    actual_waveform_sin2 =  4*numpy.sin(angular_freq*time[25000:50000])
    actual_waveform_cos3 =  5*numpy.cos(angular_freq*time[50000:75000])
    actual_waveform_sin3 = -6*numpy.sin(angular_freq*time[50000:75000])
    actual_waveform_cos4 =  7*numpy.cos(angular_freq*time[75000:100000])
    actual_waveform_sin4 =  8*numpy.sin(angular_freq*time[75000:100000])
    actual_waveform = numpy.stack([actual_waveform_cos1 + actual_waveform_sin1,
                                   actual_waveform_cos2 + actual_waveform_sin2,
                                   actual_waveform_cos3 + actual_waveform_sin3,
                                   actual_waveform_cos4 + actual_waveform_sin4]).flatten()
    actual_symbolstream = wave_detector.qam(time, actual_waveform, symbol_duration, carrier_freq)
    assert (utils.isclose(expected_symbolstream, actual_symbolstream, atol=0.1, rtol=0.05)).all()