import json
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

        self.headers = {'Content-Type': 'application/json'}
        self.response1 = self.setUpResponse(self.headers, '{"some": "json"}')
        self.response2 = self.setUpResponse(self.headers, '{"more": "json"}')
        responses = [self.response1, self.response2]

        self.multiple_response = MultipleResponse(request, responses)

        # Clear out _response since that's what we'll be validating
        self.multiple_response._response = WebObResponse()

    def setUpResponse(self, headers, body):
        if not headers:
            headers = {'Content-Type': 'application/json'}

        response = Response()
        response.status_code = 200
        response.headers = headers
        output = StringIO.StringIO()
        output.write(body)
        output.seek(0)
        response.raw = output

        return response

    def test_body(self):
        json_boolean = True
        json_null = None
        json_number = -1.1
        json_object = {"some": "json"}
        json_string = "json"
        json_array = [json_boolean, json_null, json_number, json_object,
                      json_string]

        response1 = self.setUpResponse(None, json.dumps(json_boolean))
        response2 = self.setUpResponse(None, json.dumps(json_null))
        response3 = self.setUpResponse(None, json.dumps(json_number))
        response4 = self.setUpResponse(None, json.dumps(json_object))
        response5 = self.setUpResponse(None, json.dumps(json_string))
        response_array = self.setUpResponse(None, json.dumps(json_array))

        responses = [response1, response2, response3, response4, response5,
                     response_array]
        multiple_response = MultipleResponse(self.multiple_response._request,
                                             responses)

        # Clear out _response since that's what we'll be validating
        multiple_response._response = WebObResponse()

        multiple_response._merge_responses()

        json_response = json.loads(multiple_response.response.body)

        json_booleans = filter(lambda x: x == json_boolean, json_response)
        self.assertEquals(2, len(json_booleans))

        json_nulls = filter(lambda x: x == json_null, json_response)
        self.assertEquals(2, len(json_nulls))

        json_numbers = filter(lambda x: x == json_number, json_response)
        self.assertEquals(2, len(json_numbers))

        json_objects = filter(lambda x: x == json_object, json_response)
        self.assertEquals(2, len(json_objects))

        json_strings = filter(lambda x: x == json_string, json_response)
        self.assertEquals(2, len(json_strings))

    def test_header_content_encoding(self):
        self.multiple_response._merge_responses()

        self.assertEquals(None,
                          self.multiple_response.response.content_encoding)

    def test_header_content_type(self):
        self.multiple_response._merge_responses()

        self.assertEquals(self.headers['Content-Type'],
                          self.multiple_response.response.content_type)

    def test_status(self):
        self.multiple_response._merge_responses()

        self.assertEquals(200, self.multiple_response.response.status_code)
