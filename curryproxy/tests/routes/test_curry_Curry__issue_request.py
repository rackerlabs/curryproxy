from mock import Mock
from webob import Request
from testtools import TestCase

import curry
from curry.curry import Curry
from curry.routes import route_factory


class TestCurryCurry_Issue_Request(TestCase):
    def setUp(self):
        super(TestCurryCurry_Issue_Request, self).setUp()

        self.curry = Curry('curry/tests/etc/routes.empty.json')

        self.forwarding_url_host = 'new.example.com'
        self.route_config = {'route': 'https://www.example.com',
                             'forwarding_url': 'https://' +
                             self.forwarding_url_host}
        self.route = route_factory.parse_dict(self.route_config)

        self.curry._routes.append(self.route)

        self.mock_response = Mock()
        self.mock_response.status_code = 200
        self.mock_response.headers = [('Content-Length', '7'),
                                      ('Content-Type', 'application/json'),
                                      ('Host', 'new.example.com')]
        self.mock_response.content = 'content'
        curry.routes.forwarding_route.requests.request = Mock(return_value=self.mock_response)

    def test_verify_response(self):
        request = Request.blank('https://www.example.com/test')
        response = self.curry._issue_request(request, self.route)

        self.assertEqual(self.mock_response.status_code, response.status_code)
        self.assertEqual(self.mock_response.headers, response.headerlist)
        self.assertEqual(self.mock_response.content, response.body)

    def test_verify_request(self):
        path = '/path'
        request = Request.blank('https://www.example.com' + path)
        request.headers['X-Auth-Token'] = 'Invalid'

        self.curry._issue_request(request.copy(), self.route)

        request_url = self.route_config['forwarding_url'] + path
        request.headers['Host'] = self.forwarding_url_host

        curry_request = curry.curry.requests.request
        curry_request.assert_called_with(request.method,
                                         request_url,
                                         data=request.body,
                                         headers=request.headers,
                                         allow_redirects=False,
                                         verify=True)
