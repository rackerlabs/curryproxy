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

from curryproxy import CurryProxy


class Test___Init__(testtools.TestCase):
    def setUp(self):
        super(Test___Init__, self).setUp()
        self.patcher = patch('logging.config')
        self.patcher.start()

    def test_config_default(self):
        patch_path = 'curryproxy.CurryProxy._process_routes'
        with patch(patch_path) as mocked_method:
            CurryProxy()

            default_path = '/etc/curryproxy/routes.json'
            mocked_method.assert_called_with(default_path)

    def test_config_supplied(self):
        route_file_path = 'curryproxy/tests/etc/routes.forwarding_address.json'
        curry = CurryProxy(route_file_path)

        self.assertEqual(1, len(curry._routes))

    def tearDown(self):
        super(Test___Init__, self).tearDown()
        self.patcher.stop()
