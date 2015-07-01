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


def bytes2iec(bytes, compact=False):
    """ Convert a size value in bytes to its equivalent in IEC notation.

        See `<http://physics.nist.gov/cuu/Units/binary.html>`_.

        Parameters:
            bytes (int): Number of bytes.

        Return:
            String representation of ``bytes``.

        Raises:
            ValueError: Negative or out of bounds value for ``bytes``.
    """
    postfn = lambda text: text.replace(' ', '') if compact else text
    if bytes < 0:
        raise ValueError("Negative byte size value {}".format(bytes))
    if bytes < 1024:
        return postfn('{:4d} bytes'.format(bytes))

    scaled = bytes
    for iec_unit in IEC_UNITS[1:]:
        scaled /= 1024.0
        if scaled < 1024:
            return postfn('{:6.1f} {}'.format(scaled, iec_unit))

    raise ValueError("Byte size value {} out of bounds".format(bytes))
