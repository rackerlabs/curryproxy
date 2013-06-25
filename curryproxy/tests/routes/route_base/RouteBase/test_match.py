from testtools import TestCase

from curryproxy.tests.routes.route_base.RouteBase import RouteBaseTest


class TestMatch(TestCase):
    def test_matched(self):
        class TestClass(RouteBaseTest):
            def _find_pattern_for_request(self, request_url):
                return 'url_pattern'

        route_base = TestClass()

        self.assertTrue(route_base.match(None))

    def test_unmatched(self):
        class TestClass(RouteBaseTest):
            def _find_pattern_for_request(self, request_url):
                return None

        route_base = TestClass()

        self.assertFalse(route_base.match(None))
