from testtools import ExpectedException, TestCase

from curry.curry import Curry
from curry.errors import RequestError
from curry.routes import route_factory


class TestCurryCurry_Match_Route(TestCase):
    def setUp(self):
        super(TestCurryCurry_Match_Route, self).setUp()

        self.curry = Curry('curry/tests/etc/routes.empty.json')

    def test_match(self):
        route_config = {'route': 'https://www.example.com',
                        'forwarding_url': 'https://new.example.com'}
        route = route_factory.parse_dict(route_config)

        self.curry._routes.append(route)

        matched_route = self.curry._match_route('https://www.example.com/path')

        self.assertEqual(route, matched_route)

    def test_match_first_route(self):
        route_config_1 = {'route': 'https://www.example.com',
                          'forwarding_url': 'https://1.new.example.com'}
        route_1 = route_factory.parse_dict(route_config_1)
        route_config_2 = {'route': 'https://www.example.com/path',
                          'forwarding_url': 'https://2.new.example.com'}
        route_2 = route_factory.parse_dict(route_config_2)

        self.curry._routes += [route_1, route_2]

        matched_route = self.curry._match_route('https://www.example.com/p')

        self.assertEqual(route_1, matched_route)

    def test_unmatched_no_matching_routes(self):
        route_config = {'route': 'https://www.example.com',
                        'forwarding_url': 'https://new.example.com'}
        route = route_factory.parse_dict(route_config)

        self.curry._routes.append(route)

        with ExpectedException(RequestError):
            self.curry._match_route('https://1.www.example.com/path')

    def test_unmatched_no_routes(self):
        self.assertEqual(0, len(self.curry._routes))

        with ExpectedException(RequestError):
            self.curry._match_route('https://www.example.com')
