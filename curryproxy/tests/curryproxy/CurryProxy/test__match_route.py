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

from curryproxy import CurryProxy
from curryproxy.errors import RequestError
from curryproxy.routes import route_factory


class Test_Match_Route(TestCase):
    def setUp(self):
        super(Test_Match_Route, self).setUp()

        self.curry = CurryProxy('curryproxy/tests/etc/routes.empty.json',
                                'curryproxy/tests/etc/logging.console.conf')

    def test_match(self):
        route_config = {'route': 'https://www.example.com',
                        'forwarding_url': 'https://new.example.com'}
        route = route_factory.parse_dict(route_config)

        self.curry._routes.append(route)

        matched_route = self.curry._match_route('https://www.example.com/path')

        self.assertEqual(route, matched_route)

    def test_match_first_route(self):
        route_config_1 = {'route': 'https://www.example.com',
                          'forwarding_url': 'https://1.new.example.com'}
        route_1 = route_factory.parse_dict(route_config_1)
        route_config_2 = {'route': 'https://www.example.com/path',
                          'forwarding_url': 'https://2.new.example.com'}
        route_2 = route_factory.parse_dict(route_config_2)

        self.curry._routes += [route_1, route_2]

        matched_route = self.curry._match_route('https://www.example.com/p')

        self.assertEqual(route_1, matched_route)

    def test_unmatched_no_matching_routes(self):
        route_config = {'route': 'https://www.example.com',
                        'forwarding_url': 'https://new.example.com'}
        route = route_factory.parse_dict(route_config)

        self.curry._routes.append(route)

        with ExpectedException(RequestError):
            self.curry._match_route('https://1.www.example.com/path')

    def test_unmatched_no_routes(self):
        self.assertEqual(0, len(self.curry._routes))

        with ExpectedException(RequestError):
            self.curry._match_route('https://www.example.com')
