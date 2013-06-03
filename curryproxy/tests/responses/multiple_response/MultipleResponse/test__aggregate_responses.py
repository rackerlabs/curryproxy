from mock import Mock
from requests import Response
from testtools import TestCase
from webob import Request as WebObRequest
from webob import Response as WebObResponse

from curryproxy.responses import MultipleResponse


class Test_Aggregate_Responses(TestCase):
    def setUp(self):
        super(Test_Aggregate_Responses, self).setUp()

        self.headers = {'Content-Type': 'application/json'}
        self.body_html = '<html><body><h1>Hello World</h1></body></html>'
        self.body_json = '{"some": "json"}'

    def setUpResponse(self, headers, body, status_code=200):
        if not headers:
            headers = {'Content-Type': 'application/json'}

        def decode_content():
            pass

        response = Response()
        response.status_code = status_code
        response.headers = headers
        stream = Mock()
        stream.read = Mock()
        stream.read.side_effect = [body, None]
        response.raw = stream

        return response

    def setUpMultipleResponse(self, responses):
        request = WebObRequest.blank('http://www.example.com/test')

        response = MultipleResponse(request, responses)

        # Clear out _response since that's what we'll be validating
        response._response = WebObResponse()

        return response

    def test_body(self):
        response1 = self.setUpResponse(None, self.body_json)
        response1.reason = 'OK'
        response1.url = 'http://1.example.com'
        response2 = self.setUpResponse({'Content-Type': 'text/html'},
                                       self.body_html, status_code=404)
        response2.reason = 'Not Found'
        response2.url = 'http://2.example.com'

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        response = multiple_response.response.json
        self.assertEqual(2, len(response))

        self.assertEqual(response1.url, response[0]['url'])
        self.assertEqual('200 OK', response[0]['status'])
        self.assertEqual(response1.headers, response[0]['headers'])
        self.assertEqual(self.body_json, response[0]['body'])

        self.assertEqual(response2.url, response[1]['url'])
        self.assertEqual('404 Not Found', response[1]['status'])
        self.assertEqual(response2.headers, response[1]['headers'])
        self.assertEqual(self.body_html, response[1]['body'])

    def test_content_type(self):
        headers = self.headers.copy()
        headers['Content-Type'] = 'text/html'
        response1 = self.setUpResponse(self.headers, self.body_json)
        response2 = self.setUpResponse(headers, self.body_html)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual('application/json',
                         multiple_response.response.content_type.lower())

    def test_status_code_100(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=100)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=101)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(100, multiple_response.response.status_code)

    def test_status_code_200(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=204)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=200)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(200, multiple_response.response.status_code)

    def test_status_code_200_default(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=0)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=10)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(200, multiple_response.response.status_code)

    def test_status_code_300(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=302)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=304)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(300, multiple_response.response.status_code)

    def test_status_code_400(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=200)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=404)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(400, multiple_response.response.status_code)

    def test_status_code_500(self):
        response1 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=503)
        response2 = self.setUpResponse(self.headers, self.body_json,
                                       status_code=500)

        multiple_response = self.setUpMultipleResponse([response1, response2])

        multiple_response._aggregate_responses()

        self.assertEqual(500, multiple_response.response.status_code)
