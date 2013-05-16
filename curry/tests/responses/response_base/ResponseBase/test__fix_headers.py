from mock import Mock
from webob import Response
from testtools import TestCase

from curry.responses.response_base import ResponseBase


class TestResponseBaseResponseBase_Fix_Headers(TestCase):
    def setUp(self):
        super(TestResponseBaseResponseBase_Fix_Headers, self).setUp()
        
        self.response_data = '{"test": "json"}'

        response = Response()
        response.body = self.response_data
        response.encode_content(encoding='gzip')
        self.response_data_gzipped = response.body

    def test_request_gzip_response_gzip(self):
        response = ResponseBase()
        
        response._request = Mock()
        response._request.accept_encoding = 'gzip'
        response._response = Response()
        response._response.content_encoding = 'gzip'
        response._response.body = self.response_data_gzipped

        response._fix_headers()

        self.assertEquals(self.response_data_gzipped, response._response.body)

    def test_request_gzip_response_gzip_empty(self):
        response = ResponseBase()
        
        response._request = Mock()
        response._request.accept_encoding = 'gzip'
        response._response = Response()
        response._response.content_encoding = ''
        response._response.body = self.response_data

        response._fix_headers()

        self.assertEquals(self.response_data_gzipped, response._response.body)

    def test_request_gzip_response_gzip_none(self):
        response = ResponseBase()
        
        response._request = Mock()
        response._request.accept_encoding = 'gzip'
        response._response = Response()
        response._response.content_encoding = None
        response._response.body = self.response_data

        response._fix_headers()

        self.assertEquals(self.response_data_gzipped, response._response.body)

    def test_request_gzip_empty_response_gzip(self):
        response = ResponseBase()
        
        response._request = Mock()
        response._request.accept_encoding = ''
        response._response = Response()
        response._response.content_encoding = 'gzip'
        response._response.body = self.response_data_gzipped

        response._fix_headers()

        self.assertEquals(self.response_data, response._response.body)

    def test_request_gzip_empty_response_gzip_empty(self):
        response = ResponseBase()
        
        response._request = Mock()
        response._request.accept_encoding = ''
        response._response = Response()
        response._response.content_encoding = ''
        response._response.body = self.response_data

        response._fix_headers()

        self.assertEquals(self.response_data, response._response.body)

    def test_request_gzip_empty_response_gzip_none(self):
        response = ResponseBase()
        
        response._request = Mock()
        response._request.accept_encoding = ''
        response._response = Response()
        response._response.content_encoding = None
        response._response.body = self.response_data

        response._fix_headers()

        self.assertEquals(self.response_data, response._response.body)

    def test_request_gzip_none_response_gzip(self):
        response = ResponseBase()
        
        response._request = Mock()
        response._request.accept_encoding = None
        response._response = Response()
        response._response.content_encoding = 'gzip'
        response._response.body = self.response_data_gzipped

        response._fix_headers()

        self.assertEquals(self.response_data, response._response.body)

    def test_request_gzip_none_response_gzip_empty(self):
        response = ResponseBase()
        
        response._request = Mock()
        response._request.accept_encoding = None
        response._response = Response()
        response._response.content_encoding = ''
        response._response.body = self.response_data

        response._fix_headers()

        self.assertEquals(self.response_data, response._response.body)

    def test_request_gzip_none_response_gzip_none(self):
        response = ResponseBase()
        
        response._request = Mock()
        response._request.accept_encoding = None
        response._response = Response()
        response._response.content_encoding = None
        response._response.body = self.response_data

        response._fix_headers()

        self.assertEquals(self.response_data, response._response.body)
