import pytest
import numpy
import core.radio.tx.iq_mapper as iq_mapper
import core.radio.rx.iq_demapper as iq_demapper
import core.utils.utils as utils


def test_bpsk():
    data = 0x123456789abcdef
    expected_bitstream = numpy.array(list(numpy.binary_repr(data)), dtype=numpy.int8)
    actual_symbolstream = iq_mapper.bpsk(expected_bitstream)
    actual_bitstream = iq_demapper.bpsk(actual_symbolstream)
    assert (expected_bitstream == actual_bitstream).all()

def test_qpsk():
    data = 0x123456789abcdef
    expected_bitstream = utils.zero_padder(numpy.array(list(numpy.binary_repr(data)), dtype=numpy.int8), 2)
    actual_symbolstream = iq_mapper.qpsk(expected_bitstream)
    actual_bitstream = iq_demapper.qpsk(actual_symbolstream)
    assert (expected_bitstream == actual_bitstream).all()

def test_qam16():
    data = 0x123456789abcdef
    expected_bitstream = utils.zero_padder(numpy.array(list(numpy.binary_repr(data)), dtype=numpy.int8), 4)
    actual_symbolstream = iq_mapper.qam16(expected_bitstream)
    actual_bitstream = iq_demapper.qam16(actual_symbolstream)
    assert (expected_bitstream == actual_bitstream).all()