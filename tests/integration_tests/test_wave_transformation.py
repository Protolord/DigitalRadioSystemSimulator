import pytest
import numpy
import core.radio.tx.wave_generator as wave_generator
import core.radio.rx.wave_detector as wave_detector
import core.utils.utils as utils


@pytest.fixture(scope='module')
def time():
    return numpy.linspace(0, 1, int(1e5))


def test_qam_1symbol(time):
    symbol_duration = 1
    carrier_freq = 400
    expected_symbolstream = numpy.array([1 + 1j])
    actual_signal = wave_generator.qam(
        time, expected_symbolstream, symbol_duration, carrier_freq
    )
    actual_symbolstream = wave_detector.qam(
        time, actual_signal, symbol_duration, carrier_freq
    )
    assert (utils.isclose(expected_symbolstream, actual_symbolstream)).all()


def test_qam_2symbol(time):
    symbol_duration = 0.5
    carrier_freq = 400
    expected_symbolstream = numpy.array([1 + 1j, -1 - 1j])
    actual_signal = wave_generator.qam(
        time, expected_symbolstream, symbol_duration, carrier_freq
    )
    actual_symbolstream = wave_detector.qam(
        time, actual_signal, symbol_duration, carrier_freq
    )
    assert (utils.isclose(expected_symbolstream, actual_symbolstream)).all()


def test_qam_4symbol(time):
    symbol_duration = 0.25
    carrier_freq = 400
    expected_symbolstream = numpy.array([1 + 1j, -1 - 1j, 1, -1j])
    actual_signal = wave_generator.qam(
        time, expected_symbolstream, symbol_duration, carrier_freq
    )
    actual_symbolstream = wave_detector.qam(
        time, actual_signal, symbol_duration, carrier_freq
    )
    assert (utils.isclose(expected_symbolstream, actual_symbolstream)).all()


def test_qam_8symbol(time):
    symbol_duration = 0.125
    carrier_freq = 400
    expected_symbolstream = numpy.array(
        [1 + 1j, -1 - 1j, 1, -1j, -1, 1 + 1j, -1 + 1j, 1j]
    )
    actual_signal = wave_generator.qam(
        time, expected_symbolstream, symbol_duration, carrier_freq
    )
    actual_symbolstream = wave_detector.qam(
        time, actual_signal, symbol_duration, carrier_freq
    )
    assert (utils.isclose(expected_symbolstream, actual_symbolstream)).all()
