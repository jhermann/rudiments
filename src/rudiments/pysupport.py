# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Python helpers + magic.
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
import imp
import sys


def import_name(modulename, name=None):
    """ Import identifier ``name`` from module ``modulename``.

        If ``name`` is omitted, ``modulename`` must contain the name after the
        module path, delimited by a colon.

        Parameters:
            modulename (str): Fully qualified module name, e.g. ``x.y.z``.
            name (str): Name to import from ``modulename``.

        Returns:
            object: Requested object.
    """
    if name is None:
        modulename, name = modulename.rsplit(':', 1)
    module = __import__(modulename, globals(), {}, [name])
    return getattr(module, name)


def load_module(modulename, modulepath):
    """ Load a Python module from a path under a specified name.

        Parameters:
            modulename (str): Fully qualified module name, e.g. ``x.y.z``.
            modulepath (str): Filename of the module.

        Returns:
            Loaded module.
    """
    if '.' in modulename:
        modulepackage, modulebase = modulename.rsplit('.', 1)
    else:
        modulepackage = ''

    imp.acquire_lock()
    try:
        # Check if module is already loaded
        if modulename not in sys.modules:
            # Find module on disk and try to load it
            path, name = os.path.split(modulepath)
            name = os.path.splitext(name)[0]
            handle, path, info = imp.find_module(name, [path])
            try:
                # Load the module and put into sys.modules
                module = imp.load_module(modulename, handle, path, info)
                if modulepackage:
                    setattr(sys.modules[modulepackage], modulebase, module)
            finally:
                # Make sure handle is closed properly
                if handle:
                    handle.close()
    finally:
        imp.release_lock()

    return sys.modules[modulename]
