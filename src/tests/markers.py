# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
""" py.test markers.

    For details needed to understand these tests, refer to:
        https://pytest.org/
        http://pythontesting.net/start-here/
"""
# Copyright ©  2015 - 2019 Jürgen Hermann <jh@web.de>
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


# See also setup.cfg » [pytest] » markers
cli = pytest.mark.cli
integration = pytest.mark.integration
online = pytest.mark.online


# Export all markers
__all__ = [_k
           for _k, _v in globals().items()
           if _v.__class__ is cli.__class__]
