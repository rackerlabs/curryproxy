from testtools import ExpectedException, TestCase

from curry.errors import RequestError
from curry.route import Route


class TestRouteRouteCreate_Forwarded_Url(TestCase):
    def setUp(self):
        super(TestRouteRouteCreate_Forwarded_Url, self).setUp()

        self.url_pattern = 'https://www.example.com'
        self.forwarding_url = 'https://new.example.com'
        route_config = {'route': self.url_pattern,
                        'forwarding_url': self.forwarding_url}
        self.route = Route(route_config)

    def test_matched_once(self):
        path = '/path?redirect=https://www.example.com/index.html'
        url = self.route.create_forwarded_url(self.url_pattern + path)
        self.assertEqual(self.forwarding_url + path, url)

    def test_matched_path(self):
        path = '/path?and=query#hash'
        url = self.route.create_forwarded_url(self.url_pattern + path)
        self.assertEqual(self.forwarding_url + path, url)

    def test_matched_path_empty(self):
        url = self.route.create_forwarded_url(self.url_pattern)
        self.assertEqual(self.forwarding_url, url)

    def test_unmatched(self):
        with ExpectedException(RequestError):
            self.route.create_forwarded_url('https://bad.example.com/bad')
