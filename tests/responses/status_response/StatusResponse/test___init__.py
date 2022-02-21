# Copyright (c) 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from mock import patch
from testtools import ExpectedException
from testtools import TestCase
from webob import Request

from curryproxy.responses import StatusResponse
from curryproxy.responses.response_base import ResponseBase


class Test__Init__(TestCase):
    def setUp(self):
        super(Test__Init__, self).setUp()

        self.request = Request.blank('https://www.example.com/status')

    def test__fix_headers(self):
        with patch.object(StatusResponse, '_fix_headers') as mock:
            StatusResponse(self.request)

            mock.assert_called_with()

    def test_response_body(self):
        status_response = StatusResponse(self.request)

        self.assertTrue('hostname' in status_response.response.json)

    def test_response_headers(self):
        status_response = StatusResponse(self.request)

        self.assertEqual('application/json',
                         status_response.response.headers['Content-Type'])

    def test_response_status(self):
        status_response = StatusResponse(self.request)

        self.assertEqual('200 OK', status_response.response.status)

    def test_super___init__(self):
        with patch.object(ResponseBase, '__init__') as mock:
            with ExpectedException(AttributeError):
                StatusResponse(self.request)

            mock.assert_called_with(self.request)
