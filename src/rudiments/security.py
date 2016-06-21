# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Security / AuthN / AuthZ helpers.
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
import re
import sys
import errno
import getpass
from netrc import netrc, NetrcParseError

try:
    import keyring
except ImportError:
    keyring = None

from ._compat import urlparse

__all__ = ['Credentials']


class Credentials(object):
    """Look up and provide authN credentials (username / password) from common sources."""

    URL_RE = re.compile(r'^(http|https|ftp|ftps)://')  # covers the common use cases
    NETRC_FILE = None  # use the default, unless changed for test purposes
    AUTH_MEMOIZE_INPUT = {}  # remember manual auth input across several queries in one run

    def __init__(self, target):
        """``target`` is a representation of the secured object, typically an URL."""
        self.target = target
        self.user = None
        self.password = None
        self.keyring_service = target
        self.source = None

    def auth_valid(self):
        """Return bool indicating whether full credentials were provided."""
        return bool(self.user and self.password)

    def auth_pair(self, force_console=False):
        """Return username/password tuple, possibly prompting the user for them."""
        if not self.auth_valid():
            self._get_auth(force_console)
        return (self.user, self.password)

    def _raw_input(self, prompt=None):
        """Mockable wrapper for raw_input."""
        return raw_input(prompt)  # pragma: no cover

    def _get_auth(self, force_console=False):
        """Try to get login auth from known sources."""
        if not self.target:
            raise ValueError("Unspecified target ({!r})".format(self.target))
        elif not force_console and self.URL_RE.match(self.target):
            auth_url = urlparse(self.target)
            source = 'url'
            if auth_url.username:
                self.user = auth_url.username
            if auth_url.password:
                self.password = auth_url.password
            if not self.auth_valid():
                source = self._get_auth_from_keyring()
            if not self.auth_valid():
                source = self._get_auth_from_netrc(auth_url.hostname)
            if not self.auth_valid():
                source = self._get_auth_from_console(self.target)
        else:
            source = self._get_auth_from_console(self.target)

        if self.auth_valid():
            self.source = source

    def _get_auth_from_console(self, realm):
        """Prompt for the user and password."""
        self.user, self.password = self.AUTH_MEMOIZE_INPUT.get(realm, (self.user, None))
        if not self.auth_valid():
            if not self.user:
                login = getpass.getuser()
                self.user = self._raw_input('Username for "{}" [{}]: '.format(realm, login)) or login
            self.password = getpass.getpass('Password for "{}": '.format(realm))
            Credentials.AUTH_MEMOIZE_INPUT[realm] = self.user, self.password

        return 'console'

    def _get_auth_from_netrc(self, hostname):
        """Try to find login auth in ``~/.netrc``."""
        try:
            hostauth = netrc(self.NETRC_FILE)
        except IOError as cause:
            if cause.errno != errno.ENOENT:
                raise
            return None
        except NetrcParseError as cause:
            raise  # TODO: Map to common base class, so caller has to handle less error types?

        # Try to find specific `user@host` credentials first, then just `host`
        auth = hostauth.hosts.get('{}@{}'.format(self.user or getpass.getuser(), hostname), None)
        if not auth:
            auth = hostauth.hosts.get(hostname, None)

        if auth:
            username, account, password = auth  # pylint: disable=unpacking-non-sequence
            if username:
                self.user = username
            if password == 'base64':
                # support for password obfuscation, prevent "over the shoulder lookup"
                self.password = account.decode('base64')
            elif password:
                self.password = password

        return 'netrc'

    def _get_password_from_keyring(self, accountname):
        """Query keyring for a password entry."""
        return keyring.get_password(self.keyring_service, accountname)

    def _get_auth_from_keyring(self):
        """Try to get credentials using `keyring <https://github.com/jaraco/keyring>`_."""
        if not keyring:
            return None

        # Take user from URL if available, else the OS login name
        password = self._get_password_from_keyring(self.user or getpass.getuser())
        if password is not None:
            self.user = self.user or getpass.getuser()
            self.password = password

        return 'keyring'
