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
from mock import patch
import testtools

import curryproxy
from curryproxy import CurryProxy
from curryproxy.errors import ConfigError


class Test___Init__(testtools.TestCase):
    def setUp(self):
        super(Test___Init__, self).setUp()
        self.etc = "tests/etc/"

    def test_init(self):
        curry = CurryProxy(self.etc)
        self.assertIsInstance(curry, CurryProxy)
        # FIXME: test logging/routes properly initialized...not sure
        # what else to test.

    def test_init_noetc(self):
        self.assertRaises(IOError, CurryProxy, "/dev/null")

    def test_broken_routes_file(self):
        # Replace routes.yaml with bad.yaml. Simulates a bad conf file
        # without having to keep a separate "bad" directory
        real_load = curryproxy.helpers.load

        def mocked_load(filename):
            filename = filename.replace('routes.yaml', 'bad.yaml')
            return real_load(filename)

        with patch('curryproxy.helpers.load', side_effect=mocked_load) as load:
            self.assertRaises(ConfigError, CurryProxy, self.etc)
            load.assert_called_with(self.etc + 'routes.yaml')

    def test_broken_routes_data(self):
        with patch('curryproxy.routes.make', side_effect=ConfigError):
            self.assertRaises(ConfigError, CurryProxy, self.etc)
