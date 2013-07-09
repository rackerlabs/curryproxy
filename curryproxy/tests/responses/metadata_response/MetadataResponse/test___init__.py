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
from testtools import TestCase

from curryproxy.responses import MetadataResponse
from curryproxy.tests.utils import RequestsResponseMock


class Test__Init__(TestCase):
    def test__aggregate_response_bodies(self):
        with patch.object(MetadataResponse, '_aggregate_response_bodies') as m:
            headers = {'Content-Type': 'text/html'}
            response_1 = RequestsResponseMock(status_code=200, headers=headers)
            response_2 = RequestsResponseMock(status_code=502, headers=headers)

            MetadataResponse(None, [response_1, response_2])

            m.assert_called_with()
