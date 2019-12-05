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
import unittest

from testtools import TestCase

from curryproxy.routes import EndpointsRoute


class Test_Resolve_Query_String(TestCase):
    def setUp(self):
        super(Test_Resolve_Query_String, self).setUp()

        self.route = EndpointsRoute([], [], [], [])

        self.request_base_url = 'https://1.example.com/path'

    def test_with_no_override(self):
        url = self.route._resolve_query_string(
            self.request_base_url + '?curryproxy=1:test=123,2:test=456',
            '1'
        )

        self.assertEqual(self.request_base_url + '?test=123', url)

    def test_with_override(self):
        url = self.route._resolve_query_string(
            self.request_base_url + '?test=123&curryproxy=1:test=456',
            '1'
        )

        self.assertEqual(self.request_base_url + '?test=456', url)

    def test_no_params_for_endpoint(self):
        url = self.route._resolve_query_string(
            self.request_base_url + '?curryproxy=1:test=123',
            '2'
        )

        self.assertEqual(self.request_base_url, url)

    @unittest.skip("FIXME: Broken test; fails half the time because the query "
                   "order isn't guaranteed")
    def test_multiple_parameters(self):
        url = self.route._resolve_query_string(
            self.request_base_url +
            '?curryproxy=1:test=123%26another_test=456,2:test=456',
            '1'
        )

        self.assertEqual(
            self.request_base_url + '?test=123&another_test=456',
            url
        )

    def test_multiple_curryproxy_parameters(self):
        url = self.route._resolve_query_string(
            (
                self.request_base_url +
                '?curryproxy=1:test=123&curryproxy=1:test=456'
            ),
            '1'
        )

        self.assertEqual(self.request_base_url + '?test=123', url)

    def test_upper_case_curryproxy_parameters(self):
        url = self.route._resolve_query_string(
            (
                self.request_base_url +
                '?curryproxy=A:test=123'
            ),
            'a'
        )

        self.assertEqual(self.request_base_url + '?test=123', url)
