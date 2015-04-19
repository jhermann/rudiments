# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=invalid-name
""" Test ``rudiments.reamed.click``.
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
import unittest
from contextlib import contextmanager

# import pytest

from rudiments.reamed import click
from rudiments.reamed.click import *  # pylint: disable=unused-wildcard-import


class PrettyPathTests(unittest.TestCase):

    def test_pretty_path_replaces_home_folder(self):
        path = os.path.expanduser('~/foobar')
        assert os.path.isabs(path[0]), "Test path is absolute"
        path = pretty_path(path)
        assert path[:2] == '~' + os.sep, "Path was changed to short form"
        assert path.split(os.sep) == ['~', 'foobar'], "Path is semantically the same"


class SerrorTests(unittest.TestCase):
    RECORDER = []

    @contextmanager
    def monkey_patched_secho(self):
        self.RECORDER = []
        try:
            click.secho = lambda msg, **_: self.RECORDER.append(msg)
            yield
        finally:
            click.secho = secho

    def test_serror_calls_secho(self):
        with self.monkey_patched_secho():
            click.serror("foobar")
            assert self.RECORDER[-1] == 'foobar'


    def test_serror_formats_its_message(self):
        with self.monkey_patched_secho():
            click.serror("{0} {foo}", 1, foo=2)
            assert self.RECORDER[-1] == '1 2'


class LoggedFailureTests(unittest.TestCase):

    def test_logged_failure_is_usage_error(self):
        exc = LoggedFailure("foo")
        assert isinstance(exc, UsageError), "Exception has UsageError as a base"

    def test_logged_failure_is_styled(self):
        exc = LoggedFailure("foo")
        assert exc.message[0] == '\x1b', "Message starts with ANSI sequence"
