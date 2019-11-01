import pytest
import numpy
import core.radio.tx.iq_mapper as iq_mapper
import core.radio.rx.iq_demapper as iq_demapper
import core.utils.utils as utils


@pytest.fixture(scope='module')
def bitstream():
    data = 0x123456789abcdef
    return numpy.array(list(numpy.binary_repr(data)), dtype=numpy.int8)


def test_bpsk(bitstream):
    expected_bitstream = bitstream
    actual_symbolstream = iq_mapper.bpsk(expected_bitstream)
    actual_bitstream = iq_demapper.bpsk(actual_symbolstream)
    assert (expected_bitstream == actual_bitstream).all()


def test_qpsk(bitstream):
    expected_bitstream = utils.zero_padder(bitstream, 2)
    actual_symbolstream = iq_mapper.qpsk(expected_bitstream)
    actual_bitstream = iq_demapper.qpsk(actual_symbolstream)
    assert (expected_bitstream == actual_bitstream).all()


def test_qam16(bitstream):
    expected_bitstream = utils.zero_padder(bitstream, 4)
    actual_symbolstream = iq_mapper.qam16(expected_bitstream)
    actual_bitstream = iq_demapper.qam16(actual_symbolstream)
    assert (expected_bitstream == actual_bitstream).all()
