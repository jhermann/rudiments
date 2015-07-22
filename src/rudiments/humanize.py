# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" I/O of common values in forms understood by humans.
"""
# Copyright ©  2015 Jürgen Hermann <jh@web.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, unicode_literals, print_function


IEC_UNITS = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')


def bytes2iec(size, compact=False):
    """ Convert a size value in bytes to its equivalent in IEC notation.

        See `<http://physics.nist.gov/cuu/Units/binary.html>`_.

        Parameters:
            size (int): Number of bytes.
            compact (bool): If ``True``, the result contains no spaces.

        Return:
            String representation of ``size``.

        Raises:
            ValueError: Negative or out of bounds value for ``size``.
    """
    postfn = lambda text: text.replace(' ', '') if compact else text
    if size < 0:
        raise ValueError("Negative byte size value {}".format(size))
    if size < 1024:
        return postfn('{:4d} bytes'.format(size))

    scaled = size
    for iec_unit in IEC_UNITS[1:]:
        scaled /= 1024.0
        if scaled < 1024:
            return postfn('{:6.1f} {}'.format(scaled, iec_unit))

    raise ValueError("Byte size value {} out of bounds".format(size))


def iec2bytes(size_spec, only_positive=True):
    """ Convert a size specification, optionally containing a scaling
        unit in IEC notation, to a number of bytes.

        Parameters:
            size_spec (str): Number, optionally followed by a unit.
            only_positive (bool): Allow only positive values?

        Return:
            Numeric bytes size.

        Raises:
            ValueError: Unknown unit specifiers, or bad leading integer.
    """
    scale = 1
    try:
        size = int(0 + size_spec)  # return numeric values as-is
    except (TypeError, ValueError):
        spec = size_spec.strip().lower()

        for exp, iec_unit in enumerate(IEC_UNITS[1:], 1):
            iec_unit = iec_unit.lower()
            if spec.endswith(iec_unit):
                spec = spec[:-len(iec_unit)]
                scale = 2 ** (10 * exp)
                break
            elif spec.endswith(iec_unit[0]):
                spec = spec[:-1]
                scale = 2 ** (10 * exp)
                break
        else:
            if spec.endswith('b'):
                spec = spec[:-1]

        try:
            if '.' in spec:
                size = float(spec.strip())
            else:
                size = int(spec.strip(), base=0)
        except (TypeError, ValueError) as cause:
            raise ValueError('Invalid bytes size specification {!r}: {}'.format(size_spec, cause))

    if only_positive and size < 0:
        raise ValueError('Invalid negative bytes size specification {!r}'.format(size_spec))

    return int(size * scale)


def merge_adjacent(numbers, indicator='..', base=0):
    """ Merge adjacent numbers in an iterable of numbers.

        Parameters:
            numbers (list): List of integers or numeric strings.
            indicator (str): Delimiter to indicate generated ranges.
            base (int): Passed to the `int()` conversion when comparing numbers.

        Return:
            list of str: Condensed sequence with either ranges or isolated numbers.
    """
    integers = list(sorted([(int("%s" % i, base), i) for i in numbers]))
    idx = 0
    result = []
    while idx < len(numbers):
        end = idx + 1
        while end < len(numbers) and integers[end-1][0] == integers[end][0] - 1:
            end += 1

        result.append("%s%s%s" % (integers[idx][1], indicator, integers[end-1][1])
                      if end > idx + 1
                      else "%s" % integers[idx][1])
        idx = end
    return result
