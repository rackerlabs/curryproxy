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
from mock import patch, mock_open
import testtools

from curryproxy import CurryProxy


class Test___Init__(testtools.TestCase):
    def setUp(self):
        super(Test___Init__, self).setUp()
        self.etc = "curryproxy/tests/etc"

    def test_configs_provided(self):
        routes = self.etc + "/routes.empty.yaml"
        logconf = self.etc + "/logging.conf"
        curry = CurryProxy(routes, logconf)
        self.assertIsInstance(curry, CurryProxy)

    def test_configs_from_confdir(self):
        curry = CurryProxy(confdir=self.etc)
        self.assertIsInstance(curry, CurryProxy)

    def test_routes_search_path(self):
        with patch("curryproxy.helpers.load.search") as search:
            search.return_value = {}
            # Provide logging but not routes, so it does a search
            # for routes.
            logconf = self.etc + "/logging.conf"
            CurryProxy(logging_config=logconf, confdir=self.etc)
            search.assert_called_with('routes', self.etc)

    def test_logging_search_path(self):
        with patch("curryproxy.helpers.load.search") as search:
            search.return_value = {"version" : 1}
            # Provide routes but not logging, so it does a search
            # for logging.
            routes = self.etc + "/routes.empty.yaml"
            CurryProxy(routes, confdir=self.etc)
            search.assert_called_with('logging', self.etc)
