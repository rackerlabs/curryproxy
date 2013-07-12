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
from webob import Request
from webob import Response

from curryproxy.responses.response_base import ResponseBase


class Test_Fix_Headers(TestCase):
    def test__fix_content_encoding(self):
        response = ResponseBase(None)
        response._fix_content_encoding = Mock()
        response._request = Request.blank('http://www.example.com')
        response._response = Response()

        response._fix_headers()

        response._fix_content_encoding.assert_called_with()

    def test__fix_date(self):
        response = ResponseBase(None)
        response._fix_date = Mock()
        response._request = Request.blank('http://www.example.com')
        response._response = Response()

        response._fix_headers()

        response._fix_date.assert_called_with()
