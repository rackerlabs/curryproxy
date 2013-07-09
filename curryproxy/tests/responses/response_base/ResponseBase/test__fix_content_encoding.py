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
from testtools import TestCase
from webob import Response

from curryproxy.responses.response_base import ResponseBase


class Test_Fix_Content_Encoding(TestCase):
    def setUp(self):
        super(Test_Fix_Content_Encoding, self).setUp()

        self.response_data = '{"test": "json"}'

        response = Response()
        response.body = self.response_data
        response.encode_content(encoding='gzip')
        self.response_data_gzipped = response.body

    def test_request_gzip_response_gzip(self):
        response = ResponseBase(None)

        response._request = Mock()
        response._request.accept_encoding = 'gzip'
        response._response = Response()
        response._response.content_encoding = 'gzip'
        response._response.body = self.response_data_gzipped

        response._fix_content_encoding()

        self.assertEquals(self.response_data_gzipped, response._response.body)

    def test_request_gzip_response_gzip_empty(self):
        response = ResponseBase(None)

        response._request = Mock()
        response._request.accept_encoding = 'gzip'
        response._response = Response()
        response._response.content_encoding = ''
        response._response.body = self.response_data

        response._fix_content_encoding()

        self.assertEquals(self.response_data_gzipped, response._response.body)

    def test_request_gzip_response_gzip_none(self):
        response = ResponseBase(None)

        response._request = Mock()
        response._request.accept_encoding = 'gzip'
        response._response = Response()
        response._response.content_encoding = None
        response._response.body = self.response_data

        response._fix_content_encoding()

        self.assertEquals(self.response_data_gzipped, response._response.body)

    def test_request_gzip_empty_response_gzip(self):
        response = ResponseBase(None)

        response._request = Mock()
        response._request.accept_encoding = ''
        response._response = Response()
        response._response.content_encoding = 'gzip'
        response._response.body = self.response_data_gzipped

        response._fix_content_encoding()

        self.assertEquals(self.response_data, response._response.body)

    def test_request_gzip_empty_response_gzip_empty(self):
        response = ResponseBase(None)

        response._request = Mock()
        response._request.accept_encoding = ''
        response._response = Response()
        response._response.content_encoding = ''
        response._response.body = self.response_data

        response._fix_content_encoding()

        self.assertEquals(self.response_data, response._response.body)

    def test_request_gzip_empty_response_gzip_none(self):
        response = ResponseBase(None)

        response._request = Mock()
        response._request.accept_encoding = ''
        response._response = Response()
        response._response.content_encoding = None
        response._response.body = self.response_data

        response._fix_content_encoding()

        self.assertEquals(self.response_data, response._response.body)

    def test_request_gzip_none_response_gzip(self):
        response = ResponseBase(None)

        response._request = Mock()
        response._request.accept_encoding = None
        response._response = Response()
        response._response.content_encoding = 'gzip'
        response._response.body = self.response_data_gzipped

        response._fix_content_encoding()

        self.assertEquals(self.response_data, response._response.body)

    def test_request_gzip_none_response_gzip_empty(self):
        response = ResponseBase(None)

        response._request = Mock()
        response._request.accept_encoding = None
        response._response = Response()
        response._response.content_encoding = ''
        response._response.body = self.response_data

        response._fix_content_encoding()

        self.assertEquals(self.response_data, response._response.body)

    def test_request_gzip_none_response_gzip_none(self):
        response = ResponseBase(None)

        response._request = Mock()
        response._request.accept_encoding = None
        response._response = Response()
        response._response.content_encoding = None
        response._response.body = self.response_data

        response._fix_content_encoding()

        self.assertEquals(self.response_data, response._response.body)
