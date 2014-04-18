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
from testtools import TestCase
from webob import Request as WebObRequest
from webob import Response as WebObResponse

from curryproxy.responses import MultipleResponse
from curryproxy.tests.utils import RequestsResponseMock


class Test_Aggregate_Responses(TestCase):
    def setUp(self):
        super(Test_Aggregate_Responses, self).setUp()

        self.headers = {'Content-Type': 'application/json'}
        self.body_html = '<html><body><h1>Hello World</h1></body></html>'
        self.body_json = '{"some": "json"}'

    def setUpResponse(self, headers, body, status_code=200):
        if not headers:
            headers = {'Content-Type': 'application/json'}

        def decode_content():
            pass

        response = RequestsResponseMock(status_code=status_code,
                                        headers=headers, body=body)

        return response

    def setUpMultipleResponse(self, responses):
        request = WebObRequest.blank('http://www.example.com/test')

        response = MultipleResponse(request, responses)

        # Clear out _response since that's what we'll be validating
        response._response = WebObResponse()

        return response

    def test_content_type(self):
        headers = self.headers.copy()
        headers['Content-Type'] = 'text/html'
        response1 = self.setUpResponse(self.headers, self.body_json)
        response2 = self.setUpResponse(headers, self.body_html)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual('application/json',
                         multiple_response.response.content_type.lower())

    def test_status_code_100(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=100)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=101)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(100, multiple_response.response.status_code)

    def test_status_code_200(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=204)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=200)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(200, multiple_response.response.status_code)

    def test_status_code_300(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=302)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=304)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(300, multiple_response.response.status_code)

    def test_status_code_400(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=200)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=404)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(400, multiple_response.response.status_code)

    def test_status_code_500(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=503)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=500)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(502, multiple_response.response.status_code)

    def test_status_code_502_default(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=0)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=10)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(502, multiple_response.response.status_code)

    def test_status_code_greater_than_500(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=600)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=200)
        response3 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=900)

        responses = [response1, response2, response3]
        multiple_response = self.setUpMultipleResponse(responses)

        multiple_response._aggregate_responses()

        self.assertEqual(502, multiple_response.response.status_code)
