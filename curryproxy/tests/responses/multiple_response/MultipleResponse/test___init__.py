from mock import Mock
from requests import Response
from webob import Request
from testtools import TestCase

from curryproxy.responses import MultipleResponse
from curryproxy.responses.response_base import ResponseBase


class Test__Init__(TestCase):
    def setUp(self):
        super(Test__Init__, self).setUp()

        self.request = Request.blank('http://www.example.com/test')

        self.response = Response()
        self.response.status_code = 201
        self.response.headers = {'Content-Type': 'application/json'}

    def setUp__merge_responses(self):
        #TODO: Restore these during tearDown
        MultipleResponse._aggregate_responses = Mock()
        MultipleResponse._merge_responses = Mock()

        self.request.method = 'GET'

        response1 = Response()
        response1.status_code = 200
        response1.headers['Content-Type'] = 'application/json'

        response2 = Response()
        response2.status_code = 200
        response2.headers['Content-Type'] = 'application/json'

        self.responses = [response1, response2]

    def test__fix_headers(self):
        old_call = ResponseBase._fix_headers
        ResponseBase._fix_headers = Mock()

        MultipleResponse(self.request, [self.response])

        ResponseBase._fix_headers.assert_called_with()

        ResponseBase._fix_headers = old_call

    def test__aggregate_responses_response_content_type(self):
        self.setUp__merge_responses()

        # requests library handles case insensitivity of header field names so
        # we don't need to test it here
        self.responses[0].headers['Content-Type'] = 'application/json'
        self.responses[1].headers['Content-Type'] = 'application/foo'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._aggregate_responses.assert_called_with()

    def test__aggregate_responses_response_content_type_none(self):
        self.setUp__merge_responses()

        # requests library handles case insensitivity of header field names so
        # we don't need to test it here
        self.responses[0].headers['Content-Type'] = 'application/json'
        self.responses[1].headers['Content-Type'] = None

        MultipleResponse(self.request, self.responses)

        MultipleResponse._aggregate_responses.assert_called_with()

    def test__aggregate_responses_response_status_code(self):
        self.setUp__merge_responses()

        self.responses[0].status_code = 200
        self.responses[1].status_code = 201

        MultipleResponse(self.request, self.responses)

        MultipleResponse._aggregate_responses.assert_called_with()

    def test__aggregate_responses_request_accept(self):
        self.setUp__merge_responses()

        self.request.accept = 'text/html'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._aggregate_responses.assert_called_with()

    def test__aggregate_responses_request_method(self):
        self.setUp__merge_responses()

        self.request.method = 'POST'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._aggregate_responses.assert_called_with()

    def test__merge_responses_response_content_type(self):
        self.setUp__merge_responses()

        # requests library handles case insensitivity of header field names so
        # we don't need to test it here
        self.responses[0].headers['Content-Type'] = 'application/json'
        self.responses[1].headers['Content-Type'] = 'Application/JSON'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._merge_responses.assert_called_with()

    def test__merge_responses_response_status_code(self):
        self.setUp__merge_responses()

        self.responses[0].status_code = 200
        self.responses[1].status_code = 200

        MultipleResponse(self.request, self.responses)

        MultipleResponse._merge_responses.assert_called_with()

    def test__merge_responses_request_accept(self):
        self.setUp__merge_responses()

        self.request.accept = 'application/json'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._merge_responses.assert_called_with()

    def test__merge_responses_request_accept_none(self):
        self.setUp__merge_responses()

        self.request.accept = None

        MultipleResponse(self.request, self.responses)

        MultipleResponse._merge_responses.assert_called_with()

    def test__merge_responses_request_method(self):
        self.setUp__merge_responses()

        self.request.method = 'GET'

        MultipleResponse(self.request, self.responses)

        MultipleResponse._merge_responses.assert_called_with()
