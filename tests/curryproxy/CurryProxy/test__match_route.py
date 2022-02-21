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

import curryproxy.routes.config as config
from curryproxy import CurryProxy
from curryproxy.errors import RequestError


class Test_Match_Route(TestCase):
    def setUp(self):
        super(Test_Match_Route, self).setUp()
        self.src = "https://www.example.com"
        self.tgt = "https://new.example.com"
        self.curry = CurryProxy('curryproxy/tests/etc/')
        self.forward = next(config.make({'forwards': {self.src: self.tgt}}))

    def test_match(self):
        route = self.forward
        self.curry._routes.append(route)
        matched_route = self.curry._match_route(self.src + '/path')
        self.assertEqual(route, matched_route)

    def test_match_first_route(self):
        fixme = """
        I do not think that this does what's expected. I *think* it's
        supposed to check that, if a url matches multiple routes, it
        uses the first one listed in the conf file. But 1. that behavior
        isn't documented, 2. it's not guaranteed after the conf file
        rework, and 3. This test doesn't actually test that.  The
        request string only matches one of the two routes given.

        I don't think this is a good idea anyway. If we want
        determinism, use match length or lexical sort order or
        something, not conf file order.
        """
        self.skipTest(fixme)

        route_config_1 = {'route': 'https://www.example.com',
                          'forwarding_url': 'https://1.new.example.com'}
        route_config_2 = {'route': 'https://www.example.com/path',
                          'forwarding_url': 'https://2.new.example.com'}
        conf = config.normalize([route_config_1, route_config_2])
        routes = config.make(conf)
        self.curry._routes.extend(routes)

        matched_route = self.curry._match_route('https://www.example.com/p')

        self.assertEqual(routes[0], matched_route)

    def test_unmatched_no_matching_routes(self):
        route = self.forward
        self.curry._routes.append(route)
        with ExpectedException(RequestError):
            self.curry._match_route('https://1.www.example.com/path')

    def test_unmatched_no_routes(self):
        self.curry._routes = []  # Ew
        with ExpectedException(RequestError):
            self.curry._match_route('https://www.example.com')
