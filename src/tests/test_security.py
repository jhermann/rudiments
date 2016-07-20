# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=invalid-name, unused-wildcard-import, unused-import
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
import getpass

# TODO: use mocker.call from upcoming "pytest-mock" release
try:
    from unittest.mock import call
except ImportError:
    from mock import call

import pytest

from rudiments.security import *

NETRC_TEST_CASES = [
    ('http://foo.example.com', 'john', 'doe'),
    ('http://jane@foo.example.com', 'jane', 'snafu'),
    ('https://foo.example.com', 'john', 'doe'),
    ('ftp://foo.example.com', 'john', 'doe'),
    ('ftps://foo.example.com', 'john', 'doe'),
]


def test_credentials_lookup_from_netrc_is_optional(mocker):
    mocker.patch('getpass.getpass', return_value='sesame')
    netrc = mocker.patch('rudiments.security.netrc')
    netrc.side_effect = IOError(2, "not found", "netrc")

    access = Credentials('http://jane@no-netrc.example.com')
    auth = access.auth_pair()
    assert access.source == 'console'

    with pytest.raises(IOError):
        netrc.side_effect = IOError(13, "cannot open", "netrc")
        access = Credentials('http://jane@no-netrc.example.com')
        auth = access.auth_pair()


@pytest.mark.parametrize('target', (None, ''))
def test_credentials_lookup_for_empty_target(target):
    access = Credentials(target)
    with pytest.raises(ValueError):
        auth = access.auth_pair()


def test_credentials_lookup_for_non_url_target(mocker):
    console_input = mocker.patch(__name__ + '.Credentials._raw_input', return_value='')
    mocker.patch('getpass.getpass', return_value='sesame')

    access = Credentials('some custom target')
    auth = access.auth_pair()

    console_input.assert_called_once()
    assert auth == (getpass.getuser(), 'sesame')
    assert access.source == 'console'


def test_credentials_lookup_from_console(mocker):
    console_input = mocker.patch(__name__ + '.Credentials._raw_input', return_value='')
    mocker.patch('getpass.getpass', return_value='sesame')

    access = Credentials('http://console.example.com')
    console_input.assert_not_called()
    auth = access.auth_pair()
    console_input.assert_called_once()

    assert auth == (getpass.getuser(), 'sesame')
    assert Credentials.AUTH_MEMOIZE_INPUT['http://console.example.com'] == access.auth_pair()

    # test memoization explicitly
    access = Credentials('http://console.example.com')
    auth = access.auth_pair()
    console_input.assert_called_once()

    # test with other realm
    access = Credentials('http://terminal.example.com')
    auth = access.auth_pair()
    assert console_input.call_count == 2
    assert 'http://terminal.example.com' in Credentials.AUTH_MEMOIZE_INPUT
    assert access.source == 'console'


def test_credentials_lookup_from_url():
    access = Credentials('http://jane:bar@url.example.com')
    assert access.auth_pair() == ('jane', 'bar')
    assert access.source == 'url'


@pytest.mark.parametrize('url, name, pwd', NETRC_TEST_CASES)
def test_credentials_lookup_from_netrc(datadir, url, name, pwd):
    Credentials.NETRC_FILE = os.path.join(datadir, 'netrc')
    try:
        access = Credentials(url)
        assert not access.auth_valid(), "Should be False"

        pair = access.auth_pair()
        assert name == pair[0], "Wrong username"
        assert pwd == pair[1], "Wrong password"
        assert access.auth_valid(), "Should be True"
        assert access.source == 'netrc'
    finally:
        Credentials.NETRC_FILE = None


def test_credentials_lookup_from_keyring(mocker):
    url = 'http://jane@keyring.example.com'
    get_pwd = mocker.patch('keyring.get_password', return_value='round')
    access = Credentials(url)

    assert access.auth_pair() == ('jane', 'round')
    get_pwd.assert_called_once_with(url, 'jane')
    assert access.source == 'keyring'
