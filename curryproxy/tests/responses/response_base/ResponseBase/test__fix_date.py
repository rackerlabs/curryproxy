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
from datetime import datetime

from mock import patch
from testtools import TestCase
from webob import Response

from curryproxy.responses import response_base
from curryproxy.responses.response_base import ResponseBase


class Test_Fix_Date(TestCase):
    def test__fix_date(self):
        utc_now = datetime.utcnow()

        response = ResponseBase(None)
        response._response = Response()
        response._response.date = utc_now

        mock_datetime = datetime(2012, 7, 31)
        datetime_patcher = patch.object(response_base,
                                        'datetime')
        mocked_datetime = datetime_patcher.start()
        mocked_datetime.utcnow.return_value = mock_datetime
        self.addCleanup(datetime_patcher.stop)

        response._fix_date()

        # Python cannot compare offset-naive (datetime.utcnow()) and
        # offset-aware (webob.Response.date) datetimes directly, so make a
        # naive comparison here.

        self.assertEqual(mock_datetime.year, response._response.date.year)
        self.assertEqual(mock_datetime.month, response._response.date.month)
        self.assertEqual(mock_datetime.day, response._response.date.day)
