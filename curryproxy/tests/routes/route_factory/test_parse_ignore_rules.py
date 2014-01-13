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

        self.endpoints_pattern = 'http://1.example.com/{Endpoint_IDs}/v1.0/'
        self.endpoint_1 = {"id": "1", "url": "https://1.api.example.com/v1.0/"}
        self.endpoint_2 = {"id": "2", "url": "https://2.api.example.com/v1.0/"}
        self.endpoints = [self.endpoint_1, self.endpoint_2]
        self.endpoints_config = {'route': self.endpoints_pattern,
                                 'endpoints': self.endpoints}

    def test_endpoints_ignore_errors_single_entry_valid_number(self):
        ignore_errors = ["401"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        route = route_factory.parse_dict(route_dict)

        self.assertEqual([401], route._ignore_errors)

    def test_endpoints_ignore_errors_single_entry_invalid_number(self):
        ignore_errors = ["401XYZ"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        with ExpectedException(ConfigError):
            route_factory.parse_dict(route_dict)

    def test_endpoints_ignore_errors_range_entry_valid(self):
        ignore_errors = ["401-404"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        route = route_factory.parse_dict(route_dict)

        self.assertEqual(range(401, 405), route._ignore_errors)

    def test_endpoints_ignore_errors_range_entry_invalid_separator(self):
        ignore_errors = ["401--404"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        with ExpectedException(ConfigError):
            route_factory.parse_dict(route_dict)

    def test_endpoints_ignore_errors_range_entry_invalid_start_number(self):
        ignore_errors = ["401A-404"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        with ExpectedException(ConfigError):
            route_factory.parse_dict(route_dict)

    def test_endpoints_ignore_errors_range_entry_invalid_stop_number(self):
        ignore_errors = ["401-404A"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        with ExpectedException(ConfigError):
            route_factory.parse_dict(route_dict)

    def test_endpoints_ignore_errors_single_entry_invalid_range_max(self):
        ignore_errors = ["600"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        with ExpectedException(ConfigError):
            route_factory.parse_dict(route_dict)

    def test_endpoints_ignore_errors_single_entry_valid_range_min(self):
        ignore_errors = ["0"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        route = route_factory.parse_dict(route_dict)
        self.assertEqual([0], route._ignore_errors)

    def test_endpoints_ignore_errors_range_entry_invalid_range_max(self):
        ignore_errors = ["400-600"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        with ExpectedException(ConfigError):
            route_factory.parse_dict(route_dict)

    def test_endpoints_ignore_errors_range_entry_valid_range_min(self):
        ignore_errors = ["0-400"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        route = route_factory.parse_dict(route_dict)
        self.assertEqual(range(0, 401), route._ignore_errors)

    def test_endpoints_ignore_errors_range_entry_invalid_range_reversed(self):
        ignore_errors = ["500-400"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        with ExpectedException(ConfigError):
            route_factory.parse_dict(route_dict)

    def test_endpoints_ignore_errors_missing(self):
        route = route_factory.parse_dict(self.endpoints_config)

        self.assertEqual([], route._ignore_errors)

    def test_endpoints_ignore_errors_range_entry_missing_start_number(self):
        ignore_errors = ["-404"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        with ExpectedException(ConfigError):
            route_factory.parse_dict(route_dict)

    def test_endpoints_ignore_errors_range_entry_missing_stop_number(self):
        ignore_errors = ["401-"]
        route_dict = {'route': self.endpoints_pattern,
                      'endpoints': self.endpoints,
                      'ignore_errors': ignore_errors}

        with ExpectedException(ConfigError):
            route_factory.parse_dict(route_dict)
