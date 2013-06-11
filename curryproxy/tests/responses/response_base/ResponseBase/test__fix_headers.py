from mock import Mock
from webob import Request
from webob import Response
from testtools import TestCase

from curryproxy.responses.response_base import ResponseBase


class Test_Fix_Headers(TestCase):
    def test__fix_content_encoding(self):
        response = ResponseBase(None)
        response._fix_content_encoding = Mock()
        response._request = Request.blank('http://www.example.com')
        response._response = Response()

        response._fix_headers()

        response._fix_content_encoding.assert_called_with()

    def test__fix_date(self):
        response = ResponseBase(None)
        response._fix_date = Mock()
        response._request = Request.blank('http://www.example.com')
        response._response = Response()

        response._fix_headers()

        response._fix_date.assert_called_with()
