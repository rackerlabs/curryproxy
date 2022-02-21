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
from testtools import TestCase
from webob import Request

from curryproxy.responses import SingleResponse
from curryproxy.routes import ForwardingRoute
from curryproxy.tests.utils import RequestsResponseMock


class Test__Call__(TestCase):
    def test___call__(self):
        route = ForwardingRoute(['http://example.com'], 'http://1.example.com')

        request = Request.blank('http://example.com/path')

        requests_response = RequestsResponseMock(headers={})
        requests_patcher = patch('requests.request',
                                 return_value=requests_response)
        requests_patcher.start()

        response___init__ = patch.object(SingleResponse,
                                         '__init__',
                                         return_value=None)
        sr_mock = response___init__.start()

        response_response = patch.object(SingleResponse, 'response')
        response_response.start()

        route(request)

        sr_mock.assert_called_with(request, requests_response)

        response_response.stop()
        response___init__.stop()
