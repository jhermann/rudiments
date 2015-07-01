# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation, bad-whitespace
""" Operating system related stdlib extensions.
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

# Exit codes, taken from /usr/include/sysexits.h
EX_OK          =   0 # successful termination
EX_ERROR       =   1 # unspecified error

EX_USAGE       =  64 # command line usage error
EX_DATAERR     =  65 # data format error
EX_NOINPUT     =  66 # cannot open input
EX_NOUSER      =  67 # addressee unknown
EX_NOHOST      =  68 # host name unknown
EX_UNAVAILABLE =  69 # service unavailable
EX_SOFTWARE    =  70 # internal software error
EX_OSERR       =  71 # system error (e.g., can't fork)
EX_OSFILE      =  72 # critical OS file missing
EX_CANTCREAT   =  73 # can't create (user) output file
EX_IOERR       =  74 # input/output error
EX_TEMPFAIL    =  75 # temp failure; user is invited to retry
EX_PROTOCOL    =  76 # remote error in protocol
EX_NOPERM      =  77 # permission denied
EX_CONFIG      =  78 # configuration error

EX_USER_MAX    = 113 # Maximal user-defined return code
EX_CTRL_C      = 130 # See http://www.faqs.org/docs/abs/HTML/exitcodes.html
