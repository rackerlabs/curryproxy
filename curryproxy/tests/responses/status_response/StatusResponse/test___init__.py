from testtools import ExpectedException
from mock import patch
from webob import Request
from testtools import TestCase

from curryproxy.responses.response_base import ResponseBase
from curryproxy.responses import StatusResponse


class Test__Init__(TestCase):
    def setUp(self):
        super(Test__Init__, self).setUp()

        self.request = Request.blank('https://www.example.com/status')

    def test__fix_headers(self):
        with patch.object(StatusResponse, '_fix_headers') as mock:
            StatusResponse(self.request)

            mock.assert_called_with()

    def test_response_body(self):
        status_response = StatusResponse(self.request)

        self.assertTrue('hostname' in status_response.response.json)

    def test_response_headers(self):
        status_response = StatusResponse(self.request)

        self.assertEqual('application/json',
                         status_response.response.headers['Content-Type'])

    def test_response_status(self):
        status_response = StatusResponse(self.request)

        self.assertEqual('200 OK', status_response.response.status)

    def test_super___init__(self):
        with patch.object(ResponseBase, '__init__') as mock:
            with ExpectedException(AttributeError):
                StatusResponse(self.request)

            mock.assert_called_with(self.request)
