from mock import patch
from webob import Request
from testtools import TestCase

from curryproxy.responses import ErrorResponse
from curryproxy.tests.utils import RequestsResponseMock


class Test__Init__(TestCase):
    def test_400_class_status_code(self):
        request = Request.blank('http://example.com/1')

        headers = {'Content-Type': 'text/html'}
        response_200 = RequestsResponseMock(status_code=200, headers=headers)
        response_401 = RequestsResponseMock(status_code=401, headers=headers)

        error_response = ErrorResponse(request,
                                       [response_200, response_401],
                                       [])

        self.assertEqual(401, error_response.response.status_code)

    def test_502_aggregate_response_bodies(self):
        with patch.object(ErrorResponse, '_aggregate_response_bodies') as m:
            headers = {'Content-Type': 'text/html'}
            response_1 = RequestsResponseMock(status_code=200, headers=headers)
            response_2 = RequestsResponseMock(status_code=502, headers=headers)

            ErrorResponse(None, [response_1, response_2], [])

            m.assert_called_with()

    def test_502_status_code(self):
        headers = {'Content-Type': 'text/html'}
        response_200 = RequestsResponseMock(status_code=200, headers=headers)
        response_500 = RequestsResponseMock(status_code=500, headers=headers)

        error_response = ErrorResponse(None, [response_200, response_500], [])

        self.assertEqual(502, error_response.response.status_code)

    def test_priority_error_multiple(self):
        request = Request.blank('http://example.com/1')

        headers = {'Content-Type': 'text/html'}
        response_200 = RequestsResponseMock(status_code=200, headers=headers)
        response_500 = RequestsResponseMock(status_code=404, headers=headers)
        response_401 = RequestsResponseMock(status_code=401, headers=headers)
        responses = [response_200, response_500, response_401]

        error_response = ErrorResponse(request, responses, [401, 404])

        self.assertEqual(401, error_response.response.status_code)

    def test_priority_error_multiple_first_missing(self):
        request = Request.blank('http://example.com/1')

        headers = {'Content-Type': 'text/html'}
        response_200 = RequestsResponseMock(status_code=200, headers=headers)
        response_500 = RequestsResponseMock(status_code=404, headers=headers)
        response_401 = RequestsResponseMock(status_code=401, headers=headers)
        responses = [response_200, response_500, response_401]

        error_response = ErrorResponse(request, responses, [403, 404])

        self.assertEqual(404, error_response.response.status_code)

    def test_priority_error_single(self):
        request = Request.blank('http://example.com/1')

        headers = {'Content-Type': 'text/html'}
        response_200 = RequestsResponseMock(status_code=200, headers=headers)
        response_500 = RequestsResponseMock(status_code=500, headers=headers)
        response_401 = RequestsResponseMock(status_code=401, headers=headers)
        responses = [response_200, response_500, response_401]

        error_response = ErrorResponse(request, responses, [401])

        self.assertEqual(401, error_response.response.status_code)
