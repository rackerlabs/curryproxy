from mock import Mock
from webob import Response
from testtools import TestCase

from curry.curry import Curry
from curry.routes import route_factory
from curry.tests.utils import StartResponseMock


class TestCurryCurry__Call__(TestCase):
    def setUp(self):
        super(TestCurryCurry__Call__, self).setUp()

        self.curry = Curry('curry/tests/etc/routes.empty.json')

    def test_matched_route(self):
        # Setup route
        self.route_config = {'route': 'https://www.example.com',
                             'forwarding_url': 'https://new.example.com'}
        self.route = route_factory.parse_dict(self.route_config)
        self.curry._routes.append(self.route)

        # Mocked response
        mock_response = Response()
        mock_response.status = 200
        mock_response.body = 'Response Body'
        self.route.issue_request = Mock(return_value=mock_response)

        # Create request
        environ = {'wsgi.url_scheme': 'https',
                   'HTTP_HOST': 'www.example.com',
                   'PATH_INFO': '/path',
                   'QUERY_STRING': 'query=string'}
        start_response = StartResponseMock()

        # Issue request
        response = self.curry.__call__(environ, start_response)

        # Assert
        self.assertEqual(mock_response.status, start_response.status)
        self.assertEqual(mock_response.headerlist, start_response.headers)
        self.assertEqual(mock_response.body, response)

    def test_unmatched_route(self):
        environ = {'wsgi.url_scheme': 'https',
                   'HTTP_HOST': 'www.example.com',
                   'PATH_INFO': '/path',
                   'QUERY_STRING': 'query=string'}
        start_response = StartResponseMock()

        response = self.curry.__call__(environ, start_response)

        self.assertEqual('403 Forbidden', start_response.status)
        self.assertIsNotNone(response)
