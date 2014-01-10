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
from curryproxy.routes import EndpointsRoute


class Test__Init__(TestCase):
    def test_duplicate_endpoint_ids(self):
        endpoints = {"one": "http://1.example.com/",
                     "ONE": "http://1.example.com/",
                     "two": "http://2.example.com/"}

        with ExpectedException(ConfigError):
            EndpointsRoute(None, endpoints, None, None)

    def test_endpoint_ids_lowered(self):
        endpoints = {"ONE": "http://1.example.com/",
                     "two": "http://2.example.com/"}

        endpoints_route = EndpointsRoute(None, endpoints, None, None)

        self.assertTrue('one' in endpoints_route._endpoints)
        self.assertFalse('ONE' in endpoints_route._endpoints)

    def test_forbidden_endpoint_id_asterisk(self):
        endpoints = {"one": "http://1.example.com/",
                     "*": "http://2.example.com/"}

        with ExpectedException(ConfigError):
            EndpointsRoute(None, endpoints, None, None)
