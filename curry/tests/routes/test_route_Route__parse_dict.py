from testtools import ExpectedException, TestCase

from curry.route import Route
from curry.errors import ConfigError


class TestCurryCurry_Process_Routes(TestCase):
    def setUp(self):
        super(TestCurryCurry_Process_Routes, self).setUp()

        self.setUp_route = {'route': '1', 'forwarding_url': '2'}
        self.route = Route(self.setUp_route)

    def test_route(self):
        self.assertEqual(self.setUp_route['route'], self.route._url_pattern)

    def test_dict_missing_route(self):
        with ExpectedException(ConfigError):
            self.route._parse_dict({})

    def test_forwarding_url(self):
        url_pattern = 'https://www1.example.com/'
        forwarding_url = 'https://www2.example.com/'
        route_dict = {'route': url_pattern, 'forwarding_url': forwarding_url}

        self.route._parse_dict(route_dict)

        self.assertEqual(url_pattern, self.route._url_pattern)
        self.assertEqual(forwarding_url, self.route._forwarding_url)

    def test_endpoints(self):
        url_pattern = 'https://www1.example.com/{Endpoint_IDs}'
        endpoints = [{"id": "1", "url": "https://1.api.example.com/v2.0/"}]
        route_dict = {'route': url_pattern, 'endpoints': endpoints}

        self.route._parse_dict(route_dict)

        self.assertTrue(endpoints[0]['id'] in self.route._endpoints)
        self.assertEqual(endpoints[0]['url'],
                         self.route._endpoints[endpoints[0]['id']])

    def test_endpoints_multiple(self):
        url_pattern = 'https://www1.example.com/{Endpoint_IDs}'
        endpoints = [{"id": "1", "url": "https://1.api.example.com/v2.0/"},
                     {"id": "2", "url": "https://2.api.example.com/v2.0/"}]
        route_dict = {'route': url_pattern, 'endpoints': endpoints}

        self.route._parse_dict(route_dict)

        self.assertTrue(endpoints[0]['id'] in self.route._endpoints)
        self.assertEqual(endpoints[0]['url'],
                         self.route._endpoints[endpoints[0]['id']])
        self.assertTrue(endpoints[1]['id'] in self.route._endpoints)
        self.assertEqual(endpoints[1]['url'],
                         self.route._endpoints[endpoints[1]['id']])

    def test_endpoints_missing_placeholder(self):
        url_pattern = 'https://www1.example.com/'
        endpoints = [{"id": "1", "url": "https://1.api.example.com/v2.0/"}]
        route_dict = {'route': url_pattern, 'endpoints': endpoints}

        with ExpectedException(ConfigError):
            self.route._parse_dict(route_dict)

    def test_dict_missing_forwarding_url_and_endpoints(self):
        with ExpectedException(ConfigError):
            self.route._parse_dict({'route': '1'})

    def test_dict_supplies_forwarding_url_and_endpoints(self):
        url_pattern = 'https://www1.example.com/'
        forwarding_url = 'https://www2.example.com/'
        endpoints = [{"id": "1", "url": "https://1.api.example.com/v2.0/"}]

        route_dict = {'route': url_pattern,
                      'forwarding_url': forwarding_url,
                      'endpoints': endpoints}

        with ExpectedException(ConfigError):
            self.route._parse_dict(route_dict)
