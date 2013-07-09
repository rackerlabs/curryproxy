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

from curryproxy.routes import ForwardingRoute


class Test_Find_Pattern_For_Request(TestCase):
    def setUp(self):
        super(Test_Find_Pattern_For_Request, self).setUp()

        self.forwarding_url = 'https://new.example.com'

    def test_matched_beginning(self):
        url_pattern = 'https://www.example.com'
        route = ForwardingRoute([url_pattern], self.forwarding_url)

        request_url = '{0}/path?query=true'.format(url_pattern)

        self.assertTrue(route._find_pattern_for_request(request_url))

    def test_matched_case_insensitive(self):
        url_pattern = 'https://www.example.com'
        route = ForwardingRoute([url_pattern], self.forwarding_url)

        request_url = 'https://www.example.com'.upper()

        self.assertTrue(route._find_pattern_for_request(request_url))

    def test_matched_exact(self):
        url_pattern = 'https://www.example.com'
        route = ForwardingRoute([url_pattern], self.forwarding_url)

        request_url = url_pattern

        self.assertTrue(route._find_pattern_for_request(request_url))

    def test_unmatched(self):
        url_pattern = 'https://www.example.com'
        route = ForwardingRoute([url_pattern], self.forwarding_url)

        request_url = 'https://example.com'

        self.assertIsNone(route._find_pattern_for_request(request_url))

    def test_unmatched_too_specific(self):
        url_pattern = 'https://www.example.com/path'
        route = ForwardingRoute([url_pattern], self.forwarding_url)

        request_url = 'https://www.example.com'

        self.assertIsNone(route._find_pattern_for_request(request_url))
