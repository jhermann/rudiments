# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=bad-whitespace, invalid-name
""" Test «rudiments.humanize».
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

import pytest

from rudiments import humanize

#############################################################################
# bytes2iec

def test_bytes_to_iec_negative_number():
    with pytest.raises(ValueError):
        humanize.bytes2iec(-1)


def test_bytes_to_iec_small_values():
    assert humanize.bytes2iec(   0) == '   0 bytes'
    assert humanize.bytes2iec(1023) == '1023 bytes'


def test_bytes_to_iec_compact_values():
    assert humanize.bytes2iec(0, compact=True) == '0bytes'
    assert humanize.bytes2iec(1023, compact=True) == '1023bytes'
    assert humanize.bytes2iec(1024, compact=True) == '1.0KiB'


def test_bytes_to_iec_values():
    for exp in range(1, 9):
        for val in (1, 999, 1000, 1023):
            assert humanize.bytes2iec(val * 2**(10*exp)) == '{:4d}.0 {}'.format(val, humanize.IEC_UNITS[exp])


def test_bytes_to_iec_overflow():
    assert humanize.bytes2iec(2**90 - 2**80) == '1023.0 YiB'
    with pytest.raises(ValueError):
        humanize.bytes2iec(2**90)


#############################################################################
# iec2bytes

def test_iec_to_bytes_bad_number():
    for bad in ('', '0O9', '0b2', '0xZZZ', 'abc', 'b', 'kib', ' kib'):
        with pytest.raises(ValueError):
            humanize.iec2bytes(bad)


def test_iec_to_bytes_bad_unit():
    for bad in ('bytes', 'zz', 'a', ' 0', 'zkib', 'mb'):
        with pytest.raises(ValueError):
            humanize.iec2bytes('1'+bad)


def test_iec_to_bytes_negative_numbers():
    for bad in (-1, '-1', '-42KiB'):
        assert humanize.iec2bytes(bad, only_positive=False) < 0, "{} returns negative size".format(bad)
        with pytest.raises(ValueError):
            humanize.iec2bytes(bad)


def test_iec_to_bytes_already_a_number():
    assert humanize.iec2bytes(0) == 0
    assert humanize.iec2bytes(1024) == 1024


def test_iec_to_bytes_bases():
    for spec in ('42', '0b101', '0O7', '0x42'):
        assert humanize.iec2bytes(spec) == int(spec, base=0)


def test_iec_to_bytes_with_float_value():
    assert humanize.iec2bytes('1.5K') == 1024 + 512
    assert humanize.iec2bytes('1.5B') == 1


def test_iec_to_bytes_units():
    for exp, iec_unit in enumerate(humanize.IEC_UNITS):
        assert humanize.iec2bytes('1' + iec_unit) == 2 ** (10 * exp)
        assert humanize.iec2bytes('1' + iec_unit.lower()) == 2 ** (10 * exp)
        assert humanize.iec2bytes('1' + iec_unit.upper()) == 2 ** (10 * exp)
        assert humanize.iec2bytes('1  ' + iec_unit) == 2 ** (10 * exp)
        assert humanize.iec2bytes(' 1 ' + iec_unit + ' ') == 2 ** (10 * exp)


def test_iec_to_bytes_short_units():
    for exp, iec_unit in enumerate(humanize.IEC_UNITS):
        assert humanize.iec2bytes('1' + iec_unit[0]) == 2 ** (10 * exp)


#############################################################################
# merge_adjacent

merge_adjacent_data = [
    ([], []),
    ([2, 3, 1], ["1..3"]),
    ([1, 4, 2], ["1..2", "4"]),
    (['0b1', '0o02', '0x3'], ["0b1..0x3"]),
    ([], []),
]

@pytest.mark.parametrize("numbers,expected", merge_adjacent_data)
def test_merge_adjacent_basic(numbers, expected):
    result = humanize.merge_adjacent(numbers)
    assert result == expected


def test_merge_adjacent_with_custom_indicator():
    result = humanize.merge_adjacent("123", '-')
    assert result == ["1-3"]


def test_merge_adjacent_with_explicit_base():
    result = humanize.merge_adjacent(['10', '3'], base=4)
    assert result == ["3..10"]


def test_merge_adjacent_not_numeric():
    with pytest.raises((TypeError, ValueError)):
        humanize.merge_adjacent("xyz")
