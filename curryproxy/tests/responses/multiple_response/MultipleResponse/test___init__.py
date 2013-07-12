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
from webob import Request

from curryproxy.responses import MultipleResponse
from curryproxy.responses.response_base import ResponseBase


class Test__Init__(TestCase):
    def setUp(self):
        super(Test__Init__, self).setUp()

        self.request = Request.blank('http://www.example.com/test')

        self.response = Response()
        self.response.status_code = 201
        self.response.headers = {'Content-Type': 'application/json'}

    def setUp__merge_responses(self):
        self._aggregate_responses = MultipleResponse._aggregate_responses
        self._merge_responses = MultipleResponse._merge_responses
        MultipleResponse._aggregate_responses = Mock()
        MultipleResponse._merge_responses = Mock()

        self.request.method = 'GET'

        response1 = Response()
        response1.status_code = 200
        response1.headers['Content-Type'] = 'application/json'

        response2 = Response()
        response2.status_code = 200
        response2.headers['Content-Type'] = 'application/json'

        self.responses = [response1, response2]

    def test__fix_headers(self):
        old_call = ResponseBase._fix_headers
        ResponseBase._fix_headers = Mock()

        MultipleResponse(self.request, [self.response])

        ResponseBase._fix_headers.assert_called_with()

        ResponseBase._fix_headers = old_call

    def test__aggregate_responses_response_content_type(self):
        self.setUp__merge_responses()

        # requests library handles case insensitivity of header field names so
        # we don't need to test it here
        self.responses[0].headers['Content-Type'] = 'application/json'
        self.responses[1].headers['Content-Type'] = 'application/foo'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._aggregate_responses.assert_called_with()

    def test__aggregate_responses_response_content_type_none(self):
        self.setUp__merge_responses()

        # requests library handles case insensitivity of header field names so
        # we don't need to test it here
        self.responses[0].headers['Content-Type'] = 'application/json'
        del self.responses[1].headers['Content-Type']

        MultipleResponse(self.request, self.responses)

        MultipleResponse._aggregate_responses.assert_called_with()

    def test__aggregate_responses_response_status_code(self):
        self.setUp__merge_responses()

        self.responses[0].status_code = 200
        self.responses[1].status_code = 201

        MultipleResponse(self.request, self.responses)

        MultipleResponse._aggregate_responses.assert_called_with()

    def test__aggregate_responses_request_accept(self):
        self.setUp__merge_responses()

        self.request.accept = 'text/html'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._aggregate_responses.assert_called_with()

    def test__aggregate_responses_request_method(self):
        self.setUp__merge_responses()

        self.request.method = 'POST'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._aggregate_responses.assert_called_with()

    def test__merge_responses_response_content_type(self):
        self.setUp__merge_responses()

        # requests library handles case insensitivity of header field names so
        # we don't need to test it here
        self.responses[0].headers['Content-Type'] = 'application/json'
        self.responses[1].headers['Content-Type'] = 'Application/JSON'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._merge_responses.assert_called_with()

    def test__merge_responses_response_status_code(self):
        self.setUp__merge_responses()

        self.responses[0].status_code = 200
        self.responses[1].status_code = 200

        MultipleResponse(self.request, self.responses)

        MultipleResponse._merge_responses.assert_called_with()

    def test__merge_responses_request_accept(self):
        self.setUp__merge_responses()

        self.request.accept = 'application/json'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._merge_responses.assert_called_with()

    def test__merge_responses_request_accept_none(self):
        self.setUp__merge_responses()

        self.request.accept = None

        MultipleResponse(self.request, self.responses)

        MultipleResponse._merge_responses.assert_called_with()

    def test__merge_responses_request_method(self):
        self.setUp__merge_responses()

        self.request.method = 'GET'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._merge_responses.assert_called_with()

    def tearDown(self):
        super(Test__Init__, self).tearDown()

        if hasattr(self, '_aggregate_responses'):
            MultipleResponse._aggregate_responses = self._aggregate_responses
        if hasattr(self, '_merge_responses'):
            MultipleResponse._merge_responses = self._merge_responses
