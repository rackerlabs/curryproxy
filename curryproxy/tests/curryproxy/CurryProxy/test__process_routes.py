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
from curryproxy.errors import ConfigError


class Test_Process_Routes(TestCase):
    def setUp(self):
        super(Test_Process_Routes, self).setUp()
        self.logging_conf_path = 'curryproxy/tests/etc/logging.console.conf'

    def test_config_invalid_json(self):
        with ExpectedException(ConfigError):
            CurryProxy('curryproxy/tests/etc/routes.invalid_json.json',
                       self.logging_conf_path)

    def test_config_invalid_path(self):
        with ExpectedException(IOError):
            CurryProxy('curryproxy/tests/etc/missing_file.json',
                       self.logging_conf_path)

    def test_config_valid(self):
        routes_path = 'curryproxy/tests/etc/routes.forwarding_address.json'
        curry = CurryProxy(routes_path, self.logging_conf_path)

        self.assertEqual(1, len(curry._routes))

    def test_config_multiple_routes(self):
        routes_path = 'curryproxy/tests/etc/routes.forwarding_addresses.json'
        curry = CurryProxy(routes_path, self.logging_conf_path)

        self.assertEqual(2, len(curry._routes))
