import StringIO

from requests import Response
from webob import Response as WebObResponse
from webob import Request
from testtools import TestCase

from curryproxy.responses import MultipleResponse


class Test_Merge_Responses(TestCase):
    def setUp(self):
        super(Test_Merge_Responses, self).setUp()

        request = Request.blank('http://www.example.com/test')

        response1 = self.setUpResponse('{"some": "json"}')
        response2 = self.setUpResponse('{"more": "json"}')
        responses = [response1, response2]

        self.multiple_response = MultipleResponse(request, responses)

        # Clear out _response since that's what we'll be validating
        self.multiple_response._response = WebObResponse()

    def setUpResponse(self, body):
        response = Response()
        response.status_code = 200
        response.headers = {'Content-Type': 'application/json'}
        output = StringIO.StringIO()
        output.write(body)
        output.seek(0)
        response.raw = output

        return response

    def test_status(self):
        self.multiple_response._merge_responses()

        self.assertEquals(200, self.multiple_response.response.status_code)
