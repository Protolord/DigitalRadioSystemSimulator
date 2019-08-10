import pytest
import numpy
import core.utils.utils as utils

testdata_max = [
    (complex(6, 0),   numpy.array([6, 2 + 5j, 5j, -4 + 4j, -5, -4 - 3j, -5j, 5 - 2j])),
    (complex(5, 4),   numpy.array([6, 5 + 4j, 6j, -3 + 5j, -6, -4 - 4j, -5j, 6 - 2j])),
    (complex(0, 6),   numpy.array([5, 5 + 2j, 6j, -3 + 4j, -5, -4 - 4j, -5j, 5 - 2j])),
    (complex(-4, 5),  numpy.array([6, 3 + 5j, 6j, -4 + 5j, -6, -4 - 4j, -6j, 2 - 6j])),
    (complex(-6, 0),  numpy.array([5, 5 + 2j, 5j, -5 + 3j, -6, -3 - 4j, -5j, 2 - 5j])),
    (complex(-4, -5), numpy.array([6, 4 + 3j, 6j, -6 + 2j, -6, -4 - 5j, -6j, 6 - 2j])),
    (complex(0, -6),  numpy.array([5, 2 + 5j, 5j, -4 + 3j, -5, -3 - 4j, -6j, 2 - 5j])),
    (complex(4, -5),  numpy.array([6, 4 + 4j, 6j, -2 + 6j, -6, -3 - 5j, 06j, 4 - 5j]))
]

@pytest.mark.parametrize("expected, data", testdata_max)
def test_max(expected, data):
    assert (expected == utils.max(data))

testdata_isclose = [
    # absolute tolerance
    (True,  5 + 5j,  4.6 + 4.6j, 0.4, 0),
    (False, 5 + 5j, -4.6 + 4.6j, 0.4, 0),
    (False, 5 + 5j,  4.6 - 4.6j, 0.4, 0),
    (False, 5 + 5j, -4.6 - 4.6j, 0.4, 0),
    (True,  5 + 5j,  4.8 + 4.8j, 0.2, 0),
    (False, 5 + 5j,  4.8 + 4.6j, 0.2, 0),
    (False, 5 + 5j,  4.6 + 4.6j, 0.2, 0),
    (False, 5 + 5j,  4.6 + 4.6j, 0.2, 0),
    # relative tolerance
    (True,  5 + 5j,  4.6 + 4.6j, 0, 0.10),
    (False, 5 + 5j, -4.6 + 4.6j, 0, 0.10),
    (False, 5 + 5j,  4.6 - 4.6j, 0, 0.10),
    (False, 5 + 5j, -4.6 - 4.6j, 0, 0.10),
    (False, 5 + 5j, -4.6 - 4.6j, 0, 0.10),
    (True,  5 + 5j,  4.8 + 4.8j, 0, 0.05),
    (False, 5 + 5j,  4.8 + 4.6j, 0, 0.05),
    (False, 5 + 5j,  4.6 + 4.8j, 0, 0.05),
    (False, 5 + 5j,  4.6 + 4.6j, 0, 0.05)
]

@pytest.mark.parametrize("expected, arg1, arg2, atol, rtol", testdata_isclose)
def test_isclose(expected, arg1, arg2, atol, rtol):
    assert (expected == utils.isclose(arg1, arg2, atol=atol, rtol=rtol))

testdata_zero_padder = [
    (numpy.array([1, 0]),             numpy.array([1]), 2),
    (numpy.array([1, 0, 0]),          numpy.array([1]), 3),
    (numpy.array([1, 0, 0, 0]),       numpy.array([1]), 4),
    (numpy.array([1, 0, 0, 0, 0]),    numpy.array([1]), 5),
    (numpy.array([1, 0, 0, 0, 0, 0]), numpy.array([1]), 6),

    (numpy.array([1, 1]),             numpy.array([1, 1]), 2),
    (numpy.array([1, 1, 0]),          numpy.array([1, 1]), 3),
    (numpy.array([1, 1, 0, 0]),       numpy.array([1, 1]), 4),
    (numpy.array([1, 1, 0, 0, 0]),    numpy.array([1, 1]), 5),
    (numpy.array([1, 1, 0, 0, 0, 0]), numpy.array([1, 1]), 6),

    (numpy.array([1, 1, 1, 0]),       numpy.array([1, 1, 1]), 2),
    (numpy.array([1, 1, 1]),          numpy.array([1, 1, 1]), 3),
    (numpy.array([1, 1, 1, 0]),       numpy.array([1, 1, 1]), 4),
    (numpy.array([1, 1, 1, 0, 0]),    numpy.array([1, 1, 1]), 5),
    (numpy.array([1, 1, 1, 0, 0, 0]), numpy.array([1, 1, 1]), 6),

    (numpy.array([1, 1, 1, 1]),       numpy.array([1, 1, 1, 1]), 2),
    (numpy.array([1, 1, 1, 1, 0, 0]), numpy.array([1, 1, 1, 1]), 3),
    (numpy.array([1, 1, 1, 1]),       numpy.array([1, 1, 1, 1]), 4),
    (numpy.array([1, 1, 1, 1, 0]),    numpy.array([1, 1, 1, 1]), 5),
    (numpy.array([1, 1, 1, 1, 0, 0]), numpy.array([1, 1, 1, 1]), 6)
]

@pytest.mark.parametrize("expected, data, multiple", testdata_zero_padder)
def test_zero_padder(expected, data, multiple):
    assert (expected == utils.zero_padder(data, multiple)).all()