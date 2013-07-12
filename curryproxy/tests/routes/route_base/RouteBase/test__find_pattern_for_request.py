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

from curryproxy.tests.routes.route_base.RouteBase import RouteBaseTest


class Test_Find_Pattern_For_Request(TestCase):
    def test_abstractmethod(self):
        route_base = RouteBaseTest()

        with ExpectedException(NotImplementedError):
            route_base._find_pattern_for_request(None)
