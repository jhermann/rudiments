# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" WWW access helpers.

    You need a dependency on
    `requests <http://docs.python-requests.org/en/latest/api/>`_
    in your project if you use this module.
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
import tempfile
from contextlib import contextmanager

import requests

from ._compat import urlparse, encode_filename  # pylint: disable=unused-import


__all__ = ['url_as_file']
__all__ = [encode_filename(_) for _ in __all__]


@contextmanager
def url_as_file(url, ext=None):
    """
        Context manager that GETs a given `url` and provides it as a local file.

        The file is in a closed state upon entering the context,
        and removed when leaving it, if still there.

        To give the file name a specific extension, use `ext`;
        the extension can optionally include a separating dot,
        otherwise it will be added.

        Parameters:
            url (str): URL to retrieve.
            ext (str, optional): Extension for the generated filename.

        Yields:
            str: The path to a temporary file with the content of the URL.

        Raises:
            requests.RequestException: Base exception of ``requests``, see its
                docs for more detailed ones.

        Example:
            >>> import io, re, json
            >>> with url_as_file('https://api.github.com/meta', ext='json') as meta:
            ...     meta, json.load(io.open(meta, encoding='ascii'))['hooks']
            (u'/tmp/www-api.github.com-Ba5OhD.json', [u'192.30.252.0/22'])
    """
    if ext:
        ext = '.' + ext.strip('.')  # normalize extension
    url_hint = 'www-{}-'.format(urlparse(url).hostname or 'any')

    content = requests.get(url).content
    with tempfile.NamedTemporaryFile(suffix=ext or '', prefix=url_hint, delete=False) as handle:
        handle.write(content)

    try:
        yield handle.name
    finally:
        if os.path.exists(handle.name):
            os.remove(handle.name)
