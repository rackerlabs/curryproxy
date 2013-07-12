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

from curryproxy.tests.routes.route_base.RouteBase import RouteBaseTest


class TestMatch(TestCase):
    def test_matched(self):
        class TestClass(RouteBaseTest):
            def _find_pattern_for_request(self, request_url):
                return 'url_pattern'

        route_base = TestClass()

        self.assertTrue(route_base.match(None))

    def test_unmatched(self):
        class TestClass(RouteBaseTest):
            def _find_pattern_for_request(self, request_url):
                return None

        route_base = TestClass()

        self.assertFalse(route_base.match(None))
