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
from testtools import TestCase

from curryproxy.routes import StatusRoute


class Test__Init__(TestCase):
    def test__url_patterns(self):
        url_patterns = ['https://1.example.com/status',
                        'https://2.example.com/status']

        status_route = StatusRoute(url_patterns)

        self.assertEqual(url_patterns, status_route._url_patterns)
