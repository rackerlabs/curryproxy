from mock import patch
from webob import Request
from testtools import TestCase

from curryproxy.routes import ForwardingRoute
from curryproxy.tests.utils import RequestsResponseMock
from curryproxy.responses import SingleResponse


class Test__Call__(TestCase):
    def test___call__(self):
        route = ForwardingRoute(['http://example.com'], 'http://1.example.com')

        request = Request.blank('http://example.com/path')

        requests_response = RequestsResponseMock(headers={})
        requests_patcher = patch('requests.request',
                                 return_value=requests_response)
        requests_patcher.start()

        response___init__ = patch.object(SingleResponse,
                                         '__init__',
                                         return_value=None)
        sr_mock = response___init__.start()

        response_response = patch.object(SingleResponse, 'response')
        response_response.start()

        route(request)

        sr_mock.assert_called_with(request, requests_response)

        response_response.stop()
        response___init__.stop()
