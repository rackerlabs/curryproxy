import StringIO

from mock import Mock
from requests import Response
from curry.responses.response_base import ResponseBase
from webob import Request
from testtools import TestCase

from curry.responses import SingleResponse


class TestSingleResponseSingleResponse__Init__(TestCase):
    def setUp(self):
        super(TestSingleResponseSingleResponse__Init__, self).setUp()

        self.request = Request.blank('http://www.example.com/test')

        self.response = Response()
        self.response.status_code = 201
        self.response.headers = {'Content-Type': 'application/json'}
        output = StringIO.StringIO()
        output.write('{"some": "json"}')
        self.response.raw = output

    def test__fix_headers(self):
        ResponseBase._fix_headers = Mock(return_value='test')

        SingleResponse(self.request, self.response)

        ResponseBase._fix_headers.assert_called_with()

    def test_response(self):
        single_response = SingleResponse(self.request, self.response)

        self.assertEqual(single_response._response, single_response.response)

    def test_response_status(self):
        single_response = SingleResponse(self.request, self.response)

        self.assertEqual(self.response.status_code,
                         single_response.response.status_code)

    def test_response_headers(self):
        single_response = SingleResponse(self.request, self.response)

        self.assertEqual(self.response.headers['Content-Type'],
                         single_response.response.headers['Content-Type'])

    def test_response_body(self):
        single_response = SingleResponse(self.request, self.response)

        self.assertEqual(self.response.content, single_response.response.body)

    def test_request(self):
        single_response = SingleResponse(self.request, self.response)

        self.assertEqual(self.request, single_response._request)
