import numpy


def max(array):
    max_wave = array[0]
    max_abs = numpy.abs(max_wave)
    for wave in array:
        if numpy.abs(wave) > max_abs:
            max_wave = wave
            max_abs = numpy.abs(wave)
    return max_wave


def isclose(a, b, atol=0.1, rtol=0.05):
    real = (numpy.round(numpy.abs(a.real - b.real), 15)
            <= atol + rtol*numpy.abs((a.real + b.real)/2))
    imag = (numpy.round(numpy.abs(a.imag - b.imag), 15)
            <= atol + rtol*numpy.abs((a.imag + b.imag)/2))
    return real & imag


def zero_padder(bitstream, multiple):
    mod = bitstream.size % multiple
    if 0 == mod:
        return bitstream
    return numpy.pad(bitstream, (0, multiple - mod), mode='constant')


def find_index(array, value):
    indices = numpy.where(array >= value)
    if not indices[0].size:
        return array.size - 1
    return indices[0][0]


def text_to_binary(text):
    n = int.from_bytes(text.encode(), 'big')
    return format(n, f'0{((n.bit_length()+7) // 8) * 8}b')


def binary_to_text(binary):
    text = ''
    size = 1
    for i in range(0, len(binary), 8):
        if size > 1:
            size -= 1
            continue
        if '1' == binary[i]:
            for j in range(1, 8):
                if '0' == binary[i + j]:
                    break
                size += 1
            for j in range(size - 1):
                k = i + 8*(j + 1)
                if not binary[k:].startswith('10'):
                    return text
        j = i + 8*size
        n = int(binary[i:j], 2)
        text += n.to_bytes(size, 'big').decode()
    return text


def check_input_validity(data, range_values, data_type='int'):
    if data_type == 'int':
        try:
            value = int(data)
            if int(range_values[0]) <= value <= int(range_values[1]):
                return True
        except ValueError:
            return False
    elif data_type == 'float':
        try:
            value = float(data)
            if float(range_values[0]) <= value <= float(range_values[1]):
                return True
        except ValueError:
            return False
    return False
