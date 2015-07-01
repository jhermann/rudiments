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
