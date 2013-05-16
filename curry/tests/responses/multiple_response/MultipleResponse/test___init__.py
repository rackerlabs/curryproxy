import StringIO

from mock import Mock
from requests import Response
from curry.responses.response_base import ResponseBase
from webob import Request
from testtools import TestCase

from curry.responses import MultipleResponse


class TestMultipleResponseMultipleResponse__Init__(TestCase):
    def setUp(self):
        super(TestMultipleResponseMultipleResponse__Init__, self).setUp()

        self.request = Request.blank('http://www.example.com/test')

        self.response = Response()
        self.response.status_code = 201
        self.response.headers = {'Content-Type': 'application/json'}
        output = StringIO.StringIO()
        output.write('{"some": "json"}')
        self.response.raw = output

    def test__fix_headers(self):
        ResponseBase._fix_headers = Mock(return_value='test')

        MultipleResponse(self.request, [self.response])

        ResponseBase._fix_headers.assert_called_with()

    def test__aggregate_responses(self):
        MultipleResponse._aggregate_responses = Mock()

        MultipleResponse(self.request, [self.response])

        MultipleResponse._aggregate_responses.assert_called_with()
