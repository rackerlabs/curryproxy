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
import json
import time
import uuid

import grequests
from mock import patch
from testtools import ExpectedException
from testtools import TestCase
from webob import Request

from curryproxy.helpers import ENVIRON_REQUEST_UUID_KEY
from curryproxy.responses import ErrorResponse
from curryproxy.responses import MetadataResponse
from curryproxy.responses import SingleResponse
from curryproxy.routes import EndpointsRoute
from curryproxy.tests.utils import RequestsResponseMock


class Test__Call__(TestCase):
    def setUp(self):
        super(Test__Call__, self).setUp()

        self.patcher = patch.object(grequests, 'map')
        self.grequests_map = self.patcher.start()

        url_patterns = ['http://example.com/{Endpoint_IDs}/']
        endpoint = {'test': 'http://example.com/'}
        endpoints = {'1': 'http://1.example.com/',
                     '2': 'http://2.example.com/'}
        self.endpoint_route = EndpointsRoute(url_patterns, endpoint, [])
        self.endpoints_route = EndpointsRoute(url_patterns, endpoints, [])

    def test_destination_urls(self):
        request = Request.blank('http://example.com/1,2/path')

        headers = {'Content-Type': 'application/json'}
        response = RequestsResponseMock(status_code=200, headers=headers)
        self.grequests_map.return_value = [response]

        response___init__ = patch.object(SingleResponse,
                                         '__init__',
                                         return_value=None)
        response___init__.start()

        response_response = patch.object(SingleResponse, 'response')
        response_response.start()

        response = self.endpoints_route(request)

        """Since we're mocking grequests.map(), we need to manually iterate the
            generator to achieve 100% code coverage"""
        destination_urls = list(self.grequests_map.call_args[0][0])
        self.assertEqual(2, len(destination_urls))
        for grequest_request in destination_urls:
            self.assertTrue(grequest_request.url.endswith('/path'))

        response_response.stop()
        response___init__.stop()

    def test_error_response_400(self):
        request = Request.blank('http://example.com/1,2/path')

        response1 = RequestsResponseMock(status_code=200)
        response2 = RequestsResponseMock(status_code=400)
        self.grequests_map.return_value = [response1, response2]

        route_patcher___init__ = patch.object(ErrorResponse,
                                              '__init__',
                                              return_value=None)
        route_patcher___init__.start()

        mock_response = time.time()
        route_patcher_response = patch.object(ErrorResponse,
                                              'response',
                                              new=mock_response)
        route_patcher_response.start()

        response = self.endpoints_route(request)
        self.assertEqual(mock_response, response)

        route_patcher___init__.stop()
        route_patcher_response.stop()

    def test_error_response_500(self):
        request = Request.blank('http://example.com/1,2/path')

        response1 = RequestsResponseMock(status_code=200)
        response2 = RequestsResponseMock(status_code=500)
        self.grequests_map.return_value = [response1, response2]

        route_patcher___init__ = patch.object(ErrorResponse,
                                              '__init__',
                                              return_value=None)
        route_patcher___init__.start()

        mock_response = time.time()
        route_patcher_response = patch.object(ErrorResponse,
                                              'response',
                                              new=mock_response)
        route_patcher_response.start()

        response = self.endpoints_route(request)

        self.assertEqual(mock_response, response)

        route_patcher___init__.stop()
        route_patcher_response.stop()

    def test_error_response_priority_errors(self):
        request = Request.blank('http://example.com/1,2/path')

        response1 = RequestsResponseMock(status_code=200)
        response2 = RequestsResponseMock(status_code=500)
        self.grequests_map.return_value = [response1, response2]

        route_patcher___init__ = patch.object(ErrorResponse,
                                              '__init__',
                                              return_value=None)
        error_response = route_patcher___init__.start()

        mock_response = time.time()
        route_patcher_response = patch.object(ErrorResponse,
                                              'response',
                                              new=mock_response)
        route_patcher_response.start()

        self.endpoints_route(request)

        args, kwargs = error_response.call_args
        self.assertEqual(self.endpoints_route._priority_errors, args[2])

        route_patcher___init__.stop()
        route_patcher_response.stop()

    def test_metadata_response(self):
        request_headers = {'Proxy-Aggregator-Body': 'respOnse-Metadata'}
        request = Request.blank('http://example.com/1,2/path',
                                headers=request_headers)

        headers = {'Content-Type': 'application/json'}
        response1 = RequestsResponseMock(status_code=200, headers=headers)
        response2 = RequestsResponseMock(status_code=500, headers=headers)
        self.grequests_map.return_value = [response1, response2]

        route_patcher___init__ = patch.object(MetadataResponse,
                                              '__init__',
                                              return_value=None)
        metadata_response = route_patcher___init__.start()

        mock_response = time.time()
        route_patcher_response = patch.object(MetadataResponse,
                                              'response',
                                              new=mock_response)
        route_patcher_response.start()

        self.endpoints_route(request)

        self.assertTrue(metadata_response.called)

        route_patcher___init__.stop()
        route_patcher_response.stop()

    def test_grequests_streamed(self):
        request = Request.blank('http://example.com/test/path')

        with ExpectedException(TypeError):
            self.endpoint_route(request)

        self.assertTrue({'stream': True} in self.grequests_map.call_args)

    def test_single_endpoint(self):
        request = Request.blank('http://example.com/1/path')

        headers = {'Content-Type': 'application/json'}
        response = RequestsResponseMock(status_code=200, headers=headers)
        self.grequests_map.return_value = [response]

        response___init__ = patch.object(SingleResponse,
                                         '__init__',
                                         return_value=None)
        response___init__.start()

        mock_response = time.time()
        response_response = patch.object(SingleResponse,
                                         'response',
                                         new=mock_response)
        response_response.start()

        response = self.endpoints_route(request)

        self.assertEqual(mock_response, response)

        response_response.stop()
        response___init__.stop()

    def test_timeout_body(self):
        request = Request.blank('http://example.com/1,2/path')
        request.environ[ENVIRON_REQUEST_UUID_KEY] = uuid.uuid4()

        headers = {'Content-Type': 'application/json'}
        response1 = None
        response2 = RequestsResponseMock(status_code=200,
                                         reason='OK',
                                         headers=headers)
        self.grequests_map.return_value = [response1, response2]

        response = self.endpoints_route(request)

        response_object = json.loads(response.body)
        self.assertTrue(None in response_object)
        response_200s = [i for i in response_object
                         if i is not None and i['status'] == '200 OK']
        self.assertTrue(len(response_200s) == 1)

    def test_timeout_logged(self):
        request = Request.blank('http://example.com/1,2/path')
        request.environ[ENVIRON_REQUEST_UUID_KEY] = uuid.uuid4()

        headers = {'Content-Type': 'application/json'}
        response1 = None
        response2 = RequestsResponseMock(status_code=200, headers=headers)
        self.grequests_map.return_value = [response1, response2]

        with patch('logging.error') as le:
            self.endpoints_route(request)

            self.assertTrue(le.called)

    def test_timeout_status_code(self):
        request = Request.blank('http://example.com/1,2/path')
        request.environ[ENVIRON_REQUEST_UUID_KEY] = uuid.uuid4()

        headers = {'Content-Type': 'application/json'}
        response1 = None
        response2 = RequestsResponseMock(status_code=200, headers=headers)
        self.grequests_map.return_value = [response1, response2]

        response = self.endpoints_route(request)

        self.assertEqual(504, response.status_code)

    def tearDown(self):
        super(Test__Call__, self).tearDown()

        self.patcher.stop()
