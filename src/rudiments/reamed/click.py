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
import sys

import configobj
from bunch import Bunch
from click import *  # pylint: disable=wildcard-import
from click import __all__


__all__ = tuple(__all__) + (
    'pretty_path', 'serror',
    'LoggedFailure', 'AliasedGroup', 'Configuration',
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


class Configuration(object):
    """ Configuration container that is initialized early in the main command.

        The default instance is available via the Click context as ``ctx.obj.cfg``.
        Configuration is lazily loaded, on first access.
    """

    NO_DEFAULT = object()

    @classmethod
    def from_context(cls, ctx, config_paths=None):
        """Create a configuration object, and initialize the Click context with it."""
        if ctx.obj is None:
            ctx.obj = Bunch()
        ctx.obj.cfg = cls(ctx.info_name, config_paths)
        return ctx.obj.cfg

    def __init__(self, name, config_paths=None):
        """ Set up static knowledge about configuration.

            ``config_paths`` is a list of PATHs to config files or directories.
            If that is non-empty, exactly those paths will be considered; an empty
            path element represents the default locations (just like in MANPATH).

            If the environment variable ``‹prefix›_CONFIG`` is set, its value will
            be appended to the default locations.
        """
        self.values = configobj.ConfigObj({}, encoding='utf-8', default_encoding='utf-8')
        self.name = name
        self.config_paths = []
        self.loaded = False

        env_config = os.environ.get((self.name + '-config').upper().replace('-', '_'), '')
        defaults = [
            '/etc/{}.conf'.format(self.name),
            os.path.join(get_app_dir(self.name) + '.conf'),
        ] + [i for i in env_config.split(os.pathsep) if i]

        for path in config_paths or []:
            for name in path.split(os.pathsep):
                if name:
                    self.config_paths.append(name)
                else:
                    self.config_paths.extend(defaults)

        if not self.config_paths:
            self.config_paths = defaults

    def locations(self, exists=True):
        """ Return the location of the config file(s).

            A given directory will be scanned for ``*.conf`` files, in alphabetical order.
            Any duplicates will be eliminated.

            If ``exists`` is True, only existing configuration locations are returned.
        """
        result = []
        for config_files in self.config_paths:
            if not config_files:
                continue
            if os.path.isdir(config_files):
                config_files = [os.path.join(config_files, i)
                                for i in os.listdir(config_files)
                                if i.endswith('.conf')]
            else:
                config_files = [config_files]
            for config_file in config_files:
                if not exists or os.path.exists(config_file):
                    config_file = os.path.abspath(config_file)
                    if config_file in result:
                        result.remove(config_file)
                    result.append(config_file)
        return result

    def load(self):
        """Load configuration from the defined locations."""
        if not self.loaded:
            self.values = configobj.ConfigObj({}, encoding='utf-8', default_encoding='utf-8')
            for path in self.locations():
                part = configobj.ConfigObj(infile=path, encoding='utf-8', default_encoding='utf-8')
                self.values.merge(part)
            self.loaded = True
        return self.values

    def dump(self, to=None):  # pylint: disable=invalid-name
        """Dump the merged configuration to a stream or stdout."""
        self.load().write(to or sys.stdout)

    def section(self, ctx):
        """Return section of the config for a specific context (sub-command)."""
        values = self.load()
        try:
            return values[ctx.info_name]
        except KeyError:
            raise LoggedFailure("Configuration section '{}' not found!".format(ctx.info_name))

    def get(self, name, default=NO_DEFAULT):
        """Return the specified key from the root section."""
        values = self.load()
        try:
            return values[name]
        except KeyError:
            if default is self.NO_DEFAULT:
                raise LoggedFailure("Configuration value '{}' not found in root section!".format(name))
            return default
