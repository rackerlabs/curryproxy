from datetime import datetime

from mock import patch
from webob import Response
from testtools import TestCase

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

        self.assertNotEqual(utc_now.year, response._response.date.year)
        self.assertNotEqual(utc_now.month, response._response.date.month)
        self.assertNotEqual(utc_now.day, response._response.date.day)

        self.assertEqual(mock_datetime.year, response._response.date.year)
        self.assertEqual(mock_datetime.month, response._response.date.month)
        self.assertEqual(mock_datetime.day, response._response.date.day)
