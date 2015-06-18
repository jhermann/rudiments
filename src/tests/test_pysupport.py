# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=unidiomatic-typecheck
""" Test «some_module».
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

import os

import pytest

from rudiments import pysupport


class ImportTests(object):

    def test_import_name(self):
        impname = pysupport.import_name("rudiments.pysupport", "import_name")
        assert impname is pysupport.import_name

    def test_import_name_failure(self):
        with pytest.raises(AttributeError):
            pysupport.import_name("rudiments.pysupport", "foo_bar_baz")
        with pytest.raises(ImportError):
            pysupport.import_name("foo.bar.baz", "import_name")

    def test_import_name_unary(self):
        impname = pysupport.import_name("rudiments.pysupport:import_name")
        assert impname is pysupport.import_name

    def test_import_name_unary_failure(self):
        with pytest.raises(ValueError):
            pysupport.import_name("rudiments.pysupport")

    def test_load_module(self):
        rootdir = os.path.dirname(__file__)
        while rootdir != os.path.dirname(rootdir):
            if os.path.exists(os.path.join(rootdir, "setup.py")):
                break
            rootdir = os.path.dirname(rootdir)

        lm_setup = pysupport.load_module("rudiments._lm_setup", os.path.join(rootdir, "setup.py"))
        from rudiments import _lm_setup  # pylint: disable=no-name-in-module

        assert _lm_setup is lm_setup
        assert 'project' in dir(lm_setup)
        assert type(_lm_setup.project) is dict
