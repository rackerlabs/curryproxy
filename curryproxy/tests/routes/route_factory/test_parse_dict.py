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

from curryproxy.errors import ConfigError
from curryproxy.routes import route_factory


class TestParse_Dict(TestCase):
    def setUp(self):
        super(TestParse_Dict, self).setUp()

        self.forwarding_pattern = 'http://1.example.com/v1.0/'
        self.endpoints_pattern = 'http://1.example.com/{Endpoint_IDs}/v1.0/'
        self.endpoint_1 = {"id": "1", "url": "https://1.api.example.com/v1.0/"}
        self.endpoint_2 = {"id": "2", "url": "https://2.api.example.com/v1.0/"}
        self.endpoints = [self.endpoint_1, self.endpoint_2]

        self.forwarding_config = {'route': self.forwarding_pattern,
                                  'forwarding_url': self.endpoint_1}
        self.endpoints_config = {'route': self.endpoints_pattern,
                                 'endpoints': self.endpoints}

    def test_endpoint(self):
        config = {'route': self.endpoints_pattern,
                  'endpoints': [self.endpoint_1]}

        route = route_factory.parse_dict(config)

        self.assertTrue(self.endpoint_1['id'] in route._endpoints)
        self.assertEqual(self.endpoint_1['url'],
                         route._endpoints[self.endpoint_1['id']])

    def test_endpoints(self):
        route = route_factory.parse_dict(self.endpoints_config)

        self.assertTrue(self.endpoint_1['id'] in route._endpoints)
        self.assertEqual(self.endpoint_1['url'],
                         route._endpoints[self.endpoint_1['id']])
        self.assertTrue(self.endpoint_2['id'] in route._endpoints)
        self.assertEqual(self.endpoint_2['url'],
                         route._endpoints[self.endpoint_2['id']])

    def test_endpoints_and_forwarding_url_missing(self):
        with ExpectedException(ConfigError):
            route_factory.parse_dict({'route': self.forwarding_pattern})

    def test_endpoints_and_forwarding_url_supplied(self):
        config = {'route': self.forwarding_pattern,
                  'forwarding_url': self.endpoint_1,
                  'endpoints': self.endpoints}

        with ExpectedException(ConfigError):
            route_factory.parse_dict(config)

    def test_endpoints_priority_errors(self):
        priority_errors = [401, 404]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'priority_errors': priority_errors}

        route = route_factory.parse_dict(route_dict)

        self.assertEqual(priority_errors, route._priority_errors)

    def test_endpoints_priority_errors_missing(self):
        route = route_factory.parse_dict(self.endpoints_config)

        self.assertEqual([], route._priority_errors)

    def test_endpoints_wildcard_missing(self):
        config = {'route': self.forwarding_pattern,
                  'endpoints': self.endpoints}

        with ExpectedException(ConfigError):
            route_factory.parse_dict(config)

    def test_forwarding_url(self):
        route = route_factory.parse_dict(self.forwarding_config)

        self.assertEqual(self.endpoint_1, route._forwarding_url)

    def test_route(self):
        route = route_factory.parse_dict(self.endpoints_config)

        self.assertEqual([self.endpoints_pattern], route._url_patterns)

    def test_route_missing(self):
        with ExpectedException(ConfigError):
            route_factory.parse_dict({'endpoints': self.endpoints})

    def test_status(self):
        route_dict = {'status': ['http://curryproxy.example.com/status']}

        route = route_factory.parse_dict(route_dict)

        self.assertEqual(route_dict['status'], route._url_patterns)
