"""
This module allows to write PNG files in indexed format.

use example:

palette = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 0, 255),
    (0, 255, 0)
]

image = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

import png
png.write('file.png', palette, image)
"""

import struct
import zlib

PNG_HEADER = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"

PNG_BITS_DEPTH = 8  # 8 bits PER pixel
PNG_COLOR_TYPE = 3  # indexed by palette
PNG_COMPRESSION = 0  # zlib/deflate
PNG_FILTER = 0  # basic filter (none)
PNG_INTERLACED = 0  # without interlacing
PNG_FILTER_TYPE = 0  # whitout filter
PNG_IMAGE_SIZE = 50 


def _generate_chunk(type, data):
    length = struct.pack("!I", len(data))
    crc = zlib.crc32(type + data)
    return length + type + data + struct.pack("!I", crc)


def _generate_ihdr(width, heigth):
    data = struct.pack("!IIBBBBB",
        width,
        heigth,
        PNG_BITS_DEPTH,
        PNG_COLOR_TYPE,
        PNG_COMPRESSION,
        PNG_FILTER,
        PNG_INTERLACED
    )
    return _generate_chunk(b"IHDR", data)


def _generate_plte(palette):
    data = b""
    for r, g, b in palette:
        data += struct.pack("!BBB", r, g, b)
    return _generate_chunk(b"PLTE", data)


def _generate_idat(matrix):
    data = b""
    for row in matrix:
        data += bytes([PNG_FILTER_TYPE] + row)
    return _generate_chunk(b"IDAT", zlib.compress(data))


def _generate_iend():
    return _generate_chunk(b"IEND", b"")

def write(path, palette, image):
    """
    write a file in indexed PNG format.

    Args:
        path: the path of the file to write (overwrites if already exists)
        palette: a list of tuples (r, g, b), where r, g, b are numbers between 0 and 255 inclusive.
        image: a matrix (list of rows) of integers; each number represents a pixel of the image, 
        and must be a valid index of the `palette`.
    """
    assert len(set(len(row) for row in image)) == 1, 'all rows must have the same length'

    ihdr = _generate_ihdr(len(image[0]), len(image))
    plte = _generate_plte(palette)
    idat = _generate_idat(image)
    iend = _generate_iend()

    with open(path, 'wb') as output_file:
        output_file.write(PNG_HEADER)
        output_file.write(ihdr)
        output_file.write(plte)
        output_file.write(idat)
        output_file.write(iend)

palette = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 0, 255),
    (0, 255, 0)
]

image = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


write('file.png', palette, image)