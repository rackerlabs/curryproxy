from testtools import ExpectedException, TestCase

from curry.route import Route
from curry.errors import RouteError


class TestCurryCurry_Process_Routes(TestCase):
    def setUp(self):
        super(TestCurryCurry_Process_Routes, self).setUp()

        self.setUp_route = {'route': '1', 'forwarding_uri': '2'}
        self.route = Route(self.setUp_route)

    def test_route(self):
        self.assertEqual(self.setUp_route['route'], self.route._uri_pattern)

    def test_dict_missing_route(self):
        with ExpectedException(RouteError):
            self.route._parse_dict({})

    def test_forwarding_uri(self):
        uri_pattern = 'https://www1.example.com/'
        forwarding_uri = 'https://www2.example.com/'
        route_dict = {'route': uri_pattern, 'forwarding_uri': forwarding_uri}

        self.route._parse_dict(route_dict)

        self.assertEqual(uri_pattern, self.route._uri_pattern)
        self.assertEqual(forwarding_uri, self.route._forwarding_uri)

    def test_endpoints(self):
        uri_pattern = 'https://www1.example.com/{Endpoint_IDs}'
        endpoints = [{"id": "1", "uri": "https://1.api.example.com/v2.0/"}]
        route_dict = {'route': uri_pattern, 'endpoints': endpoints}

        self.route._parse_dict(route_dict)

        self.assertTrue(endpoints[0]['id'] in self.route._endpoints)
        self.assertEqual(endpoints[0]['uri'],
                         self.route._endpoints[endpoints[0]['id']])

    def test_endpoints_multiple(self):
        uri_pattern = 'https://www1.example.com/{Endpoint_IDs}'
        endpoints = [{"id": "1", "uri": "https://1.api.example.com/v2.0/"},
                     {"id": "2", "uri": "https://2.api.example.com/v2.0/"}]
        route_dict = {'route': uri_pattern, 'endpoints': endpoints}

        self.route._parse_dict(route_dict)

        self.assertTrue(endpoints[0]['id'] in self.route._endpoints)
        self.assertEqual(endpoints[0]['uri'],
                         self.route._endpoints[endpoints[0]['id']])
        self.assertTrue(endpoints[1]['id'] in self.route._endpoints)
        self.assertEqual(endpoints[1]['uri'],
                         self.route._endpoints[endpoints[1]['id']])

    def test_endpoints_missing_placeholder(self):
        uri_pattern = 'https://www1.example.com/'
        endpoints = [{"id": "1", "uri": "https://1.api.example.com/v2.0/"}]
        route_dict = {'route': uri_pattern, 'endpoints': endpoints}

        with ExpectedException(RouteError):
            self.route._parse_dict(route_dict)

    def test_dict_missing_forwarding_uri_and_endpoints(self):
        with ExpectedException(RouteError):
            self.route._parse_dict({'route': '1'})

    def test_dict_supplies_forwarding_uri_and_endpoints(self):
        uri_pattern = 'https://www1.example.com/'
        forwarding_uri = 'https://www2.example.com/'
        endpoints = [{"id": "1", "uri": "https://1.api.example.com/v2.0/"}]

        route_dict = {'route': uri_pattern,
                      'forwarding_uri': forwarding_uri,
                      'endpoints': endpoints}

        with ExpectedException(RouteError):
            self.route._parse_dict(route_dict)
