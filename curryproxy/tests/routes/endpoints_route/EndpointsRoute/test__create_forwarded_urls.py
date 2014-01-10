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
from testtools import ExpectedException
from testtools import TestCase

from curryproxy.errors import RequestError
from curryproxy.routes import EndpointsRoute


class Test_Create_Forwarded_Urls(TestCase):
    def setUp(self):
        super(Test_Create_Forwarded_Urls, self).setUp()

        url_patterns = ['https://example.com/{Endpoint_IDs}/',
                        'https://www.example.com/{Endpoint_IDs}/']
        self.endpoints = {"one": "https://1.example.com/",
                          "two": "https://2.example.com/"}
        self.route = EndpointsRoute(url_patterns, self.endpoints, [], [])

    def test_all_endpoints(self):
        request_path = 'path'
        request_url = 'https://example.com/*/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)

    def test_case_insensitivity(self):
        request_path = 'path'
        request_url = 'https://example.com/one,TwO/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)

    def test_invalid_endpoint(self):
        request_path = 'path'
        request_url = 'https://example.com/1/' + request_path

        with ExpectedException(RequestError):
            self.route._create_forwarded_urls(request_url)

    def test_single_endpoint(self):
        request_path = 'path'
        request_url = 'https://example.com/one/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        two_url = self.endpoints['two'] + request_path
        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(two_url not in forwarded_urls)

    def test_whitespace_encoded_leading(self):
        request_path = 'path'
        request_url = 'https://example.com/%20one,%20two/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)

    def test_whitespace_encoded_trailing(self):
        request_path = 'path'
        request_url = 'https://example.com/one%20,two%20/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)

    def test_whitespace_leading(self):
        request_path = 'path'
        request_url = 'https://example.com/ one, two/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)

    def test_whitespace_trailing(self):
        request_path = 'path'
        request_url = 'https://example.com/one ,two /' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)
