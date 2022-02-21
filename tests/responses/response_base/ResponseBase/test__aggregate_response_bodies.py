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
from mock import Mock
from requests import Response
from testtools import TestCase
from webob import Request as WebObRequest
from webob import Response as WebObResponse

from curryproxy.responses import MultipleResponse
from curryproxy.responses.response_base import ResponseBase
from curryproxy.tests.utils import RequestsResponseMock


class Test_Aggregate_Response_Bodies(TestCase):

    def setUpResponse(self, headers, body, status_code=200):
        if not headers:
            headers = {'Content-Type': 'application/json'}

        def decode_content():
            pass

        response = Response()
        response.status_code = status_code
        response.headers = headers
        stream = Mock()
        stream.read = Mock()
        stream.read.side_effect = [body, None]
        response.raw = stream

        return response

    def setUpMultipleResponse(self, responses):
        request = WebObRequest.blank('http://www.example.com/test')

        response = MultipleResponse(request, responses)

        # Clear out _response since that's what we'll be validating
        response._response = WebObResponse()

        return response

    def test_body(self):
        url_1 = 'http://1.example.com'
        status_code_1 = 200
        reason_1 = 'OK'
        headers_1 = {'Content-Type': 'text/html'}
        body_1 = '<html><body><h1>Hello World</h1></body></html>'
        response_html = RequestsResponseMock(url_1,
                                             status_code_1,
                                             reason_1,
                                             headers_1,
                                             body_1)

        url_2 = 'http://2.example.com'
        status_code_2 = 404
        reason_2 = 'Custom Not Found'
        headers_2 = {'Content-Type': 'application/json'}
        body_2 = '{"some": "json"}'
        response_json = RequestsResponseMock(url_2,
                                             status_code_2,
                                             reason_2,
                                             headers_2,
                                             body_2)

        response_base = ResponseBase(None)
        response_base._responses = [response_html, response_json, None]

        response_base._aggregate_response_bodies()

        response = response_base.response.json
        self.assertEqual(
            'application/json',
            response_base.response.content_type,
        )
        self.assertEqual(3, len(response))

        self.assertEqual(url_1, response[0]['url'])
        self.assertEqual('{0} {1}'.format(status_code_1, reason_1),
                         response[0]['status'])
        self.assertEqual(headers_1, response[0]['headers'])
        self.assertEqual(body_1, response[0]['body'])

        self.assertEqual(url_2, response[1]['url'])
        self.assertEqual('{0} {1}'.format(status_code_2, reason_2),
                         response[1]['status'])
        self.assertEqual(headers_2, response[1]['headers'])
        self.assertEqual(body_2, response[1]['body'])

        self.assertIsNone(response[2])
