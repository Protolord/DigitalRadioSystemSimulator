import numpy
import core.radio.tx.iq_mapper as iq_mapper
import core.utils.utils as utils


def test_bpsk_mapping():
    expected_symbolstream = numpy.array([1 + 1j, -1 - 1j])/numpy.sqrt(2)
    actual_bitstream = numpy.array([0, 1])
    actual_symbolstream = iq_mapper.bpsk(actual_bitstream)
    results = utils.isclose(
        expected_symbolstream, actual_symbolstream, atol=0.01, rtol=0.01
    )
    assert (results).all()


def test_qpsk_mapping():
    expected_symbolstream = numpy.array(
        [1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]
    )/numpy.sqrt(2)
    actual_bitstream = numpy.array(
          [0, 0,   0, 1,    1, 0,    1, 1]
    )
    actual_symbolstream = iq_mapper.qpsk(actual_bitstream)
    results = utils.isclose(
        expected_symbolstream, actual_symbolstream, atol=0.01, rtol=0.01
    )
    assert (results).all()


def test_qam16_mapping():
    expected_symbolstream = numpy.array(
           [+1 + 1j,      1 + 3j,      3 + 1j,      3 + 3j,
            +1 - 1j,      1 - 3j,      3 - 1j,      3 - 3j,
            -1 + 1j,     -1 + 3j,     -3 + 1j,     -3 + 3j,
            -1 - 1j,     -1 - 3j,     -3 - 1j,     -3 - 3j]
    )/numpy.sqrt(10)
    actual_bitstream = numpy.array(
        [0, 0, 0, 0,  0, 0, 0, 1,  0, 0, 1, 0,  0, 0, 1, 1,
         0, 1, 0, 0,  0, 1, 0, 1,  0, 1, 1, 0,  0, 1, 1, 1,
         1, 0, 0, 0,  1, 0, 0, 1,  1, 0, 1, 0,  1, 0, 1, 1,
         1, 1, 0, 0,  1, 1, 0, 1,  1, 1, 1, 0,  1, 1, 1, 1]
    )
    actual_symbolstream = iq_mapper.qam16(actual_bitstream)
    results = utils.isclose(
        expected_symbolstream, actual_symbolstream, atol=0.01, rtol=0.01
    )
    assert (results).all()
