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
from curryproxy.routes import ForwardingRoute


class Test_Create_Forwarded_Url(TestCase):
    def setUp(self):
        super(Test_Create_Forwarded_Url, self).setUp()

        self.url_patterns = ['https://www.example.com']
        self.forwarding_url = 'https://new.example.com'
        self.forwarding_route = ForwardingRoute(self.url_patterns,
                                                self.forwarding_url)

    def test_matched_once(self):
        path = '/path?redirect={0}/index.html'.format(self.url_patterns[0])
        url = self.url_patterns[0] + path

        forwarded_url = self.forwarding_route._create_forwarded_url(url)

        self.assertEqual(self.forwarding_url + path, forwarded_url)

    def test_matched_path(self):
        path = '/path?and=query#hash'
        url = self.url_patterns[0] + path

        forwarded_url = self.forwarding_route._create_forwarded_url(url)

        self.assertEqual(self.forwarding_url + path, forwarded_url)

    def test_matched_path_empty(self):
        url = self.url_patterns[0]

        forwarded_url = self.forwarding_route._create_forwarded_url(url)

        self.assertEqual(self.forwarding_url, forwarded_url)

    def test_unmatched(self):
        with ExpectedException(RequestError):
            url = 'https://bad.example.com/bad'

            self.forwarding_route._create_forwarded_url(url)
