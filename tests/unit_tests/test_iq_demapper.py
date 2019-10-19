import pytest
import numpy
import core.radio.rx.iq_demapper as iq_demapper
import core.utils.utils as utils


def test_bpsk_demapping():
    expected_bitstream = numpy.array([0, 1])
    actual_symbolstream = numpy.array([1 + 1j, -1 - 1j])/numpy.sqrt(2)
    actual_bitstream = iq_demapper.bpsk(actual_symbolstream)
    assert (expected_bitstream == actual_bitstream).all()


def test_qpsk_demapping():
    expected_bitstream = numpy.array([0, 0,  0, 1,  1, 0,  1, 1])
    actual_symbolstream = numpy.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j])/numpy.sqrt(2)
    actual_bitstream = iq_demapper.qpsk(actual_symbolstream)
    assert (expected_bitstream == actual_bitstream).all()

def test_qam16_demapping():
    expected_bitstream = numpy.array([0, 0, 0, 0,  0, 0, 0, 1,  0, 0, 1, 0,  0, 0, 1, 1,
                                      0, 1, 0, 0,  0, 1, 0, 1,  0, 1, 1, 0,  0, 1, 1, 1,
                                      1, 0, 0, 0,  1, 0, 0, 1,  1, 0, 1, 0,  1, 0, 1, 1,
                                      1, 1, 0, 0,  1, 1, 0, 1,  1, 1, 1, 0,  1, 1, 1, 1])
    actual_symbolstream = numpy.array([ 1 + 1j,  1 + 3j,  3 + 1j,  3 + 3j,
                                        1 - 1j,  1 - 3j,  3 - 1j,  3 - 3j,
                                       -1 + 1j, -1 + 3j, -3 + 1j, -3 + 3j,
                                       -1 - 1j, -1 - 3j, -3 - 1j, -3 - 3j])/numpy.sqrt(10)
    actual_bitstream = iq_demapper.qam16(actual_symbolstream)
    assert (expected_bitstream == actual_bitstream).all()