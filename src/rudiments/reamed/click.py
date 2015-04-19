# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" ‘Double Click’ – Extensions to Click.
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

from click import *  # pylint: disable=wildcard-import
from click import __all__

__all__ = tuple(__all__) + (
    'pretty_path', 'serror',
    'LoggedFailure', 'AliasedGroup',
)


def pretty_path(path, _home_re=re.compile('^' + re.escape(os.path.expanduser('~') + os.sep))):
    """Prettify path for humans, and make it Unicode."""
    path = format_filename(path)
    path = _home_re.sub('~' + os.sep, path)
    return path


def serror(message, *args, **kwargs):
    """Print a styled error message, while using any arguments to format the message."""
    if args or kwargs:
        message = message.format(*args, **kwargs)
    return secho(message, fg='white', bg='red', bold=True)


class LoggedFailure(UsageError):
    """Report a failure condition to the user."""

    def __init__(self, message):
        message = style(message, fg='white', bg='red', bold=True)
        UsageError.__init__(self, message)


class AliasedGroup(Group):
    """ A command group with alias names.

        Inherit from this class and define a ``MAP`` class variable,
        which is a mapping from alias names to canonical command names.
        Then use that derived class as the ``cls`` parameter for a
        ``click.group`` decorator.
    """

    MAP = {}

    def get_command(self, ctx, cmd_name):
        """Map some aliases to their 'real' names."""
        cmd_name = self.MAP.get(cmd_name, cmd_name)
        return Group.get_command(self, ctx, cmd_name)
