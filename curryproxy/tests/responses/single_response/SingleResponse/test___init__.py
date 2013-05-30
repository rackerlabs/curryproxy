import StringIO

from mock import Mock
from requests import Response
from webob import Request
from testtools import TestCase

from curryproxy.responses.response_base import ResponseBase
from curryproxy.responses import SingleResponse


class Test__Init__(TestCase):
    def setUp(self):
        super(Test__Init__, self).setUp()

        self.request = Request.blank('http://www.example.com/test')

        self.response = Response()
        self.response.status_code = 201
        self.response.reason = 'Created Custom'
        self.response.headers = {'Content-Type': 'application/json'}
        self.response_body = '{"some": "json"}'
        output = StringIO.StringIO()
        output.write(self.response_body)
        output.seek(0)
        self.response.raw = output

    def test__fix_headers(self):
        old_call = ResponseBase._fix_headers
        ResponseBase._fix_headers = Mock()

        SingleResponse(self.request, self.response)

        ResponseBase._fix_headers.assert_called_with()

        ResponseBase._fix_headers = old_call

    def test_response(self):
        single_response = SingleResponse(self.request, self.response)

        self.assertEqual(single_response._response, single_response.response)

    def test_response_status(self):
        single_response = SingleResponse(self.request, self.response)

        expected_status = '{0} {1}'.format(self.response.status_code,
                                           self.response.reason)

        self.assertEqual(expected_status, single_response.response.status)

    def test_response_headers(self):
        single_response = SingleResponse(self.request, self.response)

        self.assertEqual(self.response.headers['Content-Type'],
                         single_response.response.headers['Content-Type'])

    def test_response_body(self):
        single_response = SingleResponse(self.request, self.response)

        self.assertEqual(self.response_body, single_response.response.body)

    def test_request(self):
        single_response = SingleResponse(self.request, self.response)

        self.assertEqual(self.request, single_response._request)
