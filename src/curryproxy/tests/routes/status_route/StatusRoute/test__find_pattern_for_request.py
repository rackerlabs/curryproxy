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

from curryproxy.routes import StatusRoute


class Test_Find_Pattern_For_Request(TestCase):
    def setUp(self):
        super(Test_Find_Pattern_For_Request, self).setUp()

        self.url_patterns = ['https://www.example.com/status']

    def test_request_url_matched(self):
        status_route = StatusRoute(self.url_patterns)

        request_url = 'https://www.example.com/status'
        found_pattern = status_route._find_pattern_for_request(request_url)

        self.assertTrue(found_pattern)

    def test_request_url_unmatched(self):
        status_route = StatusRoute(self.url_patterns)

        request_url = 'https://www.example.com/status2'
        found_pattern = status_route._find_pattern_for_request(request_url)

        self.assertEqual(None, found_pattern)
