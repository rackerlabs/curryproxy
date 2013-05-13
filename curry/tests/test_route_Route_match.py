from testtools import TestCase

from curry.route import Route


class TestRouteRouteMatch(TestCase):
    def setUp(self):
        super(TestRouteRouteMatch, self).setUp()

        self.route_config = {'forwarding_url': 'https://new.example.com'}

    def test_matched_beginning(self):
        self.route_config['route'] = 'https://www.example.com'
        route = Route(self.route_config)

        self.assertTrue(route.match('https://www.example.com/path?query=true'))

    def test_matched_case_insensitive(self):
        self.route_config['route'] = 'https://www.EXAMPLE.com'
        route = Route(self.route_config)

        self.assertTrue(route.match('https://www.example.com'))

    def test_matched_exact(self):
        self.route_config['route'] = 'https://www.example.com'
        route = Route(self.route_config)

        self.assertTrue(route.match('https://www.example.com'))

    def test_unmatched(self):
        self.route_config['route'] = 'https://www.example.com'
        route = Route(self.route_config)

        self.assertFalse(route.match('https://www.rackspace.com'))

    def test_unmatched_too_specific(self):
        self.route_config['route'] = 'https://www.example.com/path'
        route = Route(self.route_config)

        self.assertFalse(route.match('https://www.example.com'))
