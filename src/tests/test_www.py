# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation, invalid-name
# pylint: disable=unused-wildcard-import
""" Test ``rudiments.www``.
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
from contextlib import contextmanager

# import pytest
import responses

from rudiments.www import *


class URLAsFileTests(object):

    URL = 'http://example.com/index.html'
    BODY = 'Hi there!'

    @contextmanager
    def index_html(self):
        mock = responses.RequestsMock()
        mock.start()
        try:
            mock.add(mock.GET, self.URL, status=200, content_type='text/plain', body=self.BODY)
            yield mock
        finally:
            mock.stop()
            mock.reset()

    def test_url_as_file_works(self):
        with self.index_html():
            with url_as_file(self.URL, ext='html') as filename:
                assert os.path.getsize(filename) == len(self.BODY)
                assert 'example.com' in filename
                assert filename.endswith('.html')

    def test_url_as_file_cleanup_survives_file_deletion(self):
        with self.index_html():
            with url_as_file(self.URL) as filename:
                os.remove(filename)
                # if the context manager now raises, pytest will fail this

    def test_url_as_file_without_extension(self):
        with self.index_html():
            with url_as_file(self.URL) as filename:
                assert '.' not in os.path.basename(filename).replace('.com', '')
