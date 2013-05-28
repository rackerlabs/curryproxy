from datetime import datetime
import time

from webob import Response
from testtools import TestCase

from curryproxy.responses.response_base import ResponseBase


class Test_Fix_Date(TestCase):
    def test__fix_date(self):
        utc_now = datetime.utcnow()

        response = ResponseBase()
        response._response = Response()
        response._response.date = utc_now

        # Ensure a second has passed before fixing the Date header
        time.sleep(1)

        response._fix_date()

        """
        Unfortunately, Python cannot compare offset-naive and offset-aware
        datetimes directly. webob.Response.date is only accurate to the second,
        so just make sure we have a new value there.
        """

        self.assertNotEquals(utc_now.second, response._response.date.second)
