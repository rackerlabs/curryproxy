from testtools import TestCase

from curryproxy.routes import ForwardingRoute


class Test_Find_Pattern_For_Request(TestCase):
    def setUp(self):
        super(Test_Find_Pattern_For_Request, self).setUp()

        self.forwarding_url = 'https://new.example.com'

    def test_matched_beginning(self):
        url_pattern = 'https://www.example.com'
        route = ForwardingRoute([url_pattern], self.forwarding_url)

        request_url = '{0}/path?query=true'.format(url_pattern)

        self.assertTrue(route._find_pattern_for_request(request_url))

    def test_matched_case_insensitive(self):
        url_pattern = 'https://www.example.com'
        route = ForwardingRoute([url_pattern], self.forwarding_url)

        request_url = 'https://www.example.com'.upper()

        self.assertTrue(route._find_pattern_for_request(request_url))

    def test_matched_exact(self):
        url_pattern = 'https://www.example.com'
        route = ForwardingRoute([url_pattern], self.forwarding_url)

        request_url = url_pattern

        self.assertTrue(route._find_pattern_for_request(request_url))

    def test_unmatched(self):
        url_pattern = 'https://www.example.com'
        route = ForwardingRoute([url_pattern], self.forwarding_url)

        request_url = 'https://example.com'

        self.assertIsNone(route._find_pattern_for_request(request_url))

    def test_unmatched_too_specific(self):
        url_pattern = 'https://www.example.com/path'
        route = ForwardingRoute([url_pattern], self.forwarding_url)

        request_url = 'https://www.example.com'

        self.assertIsNone(route._find_pattern_for_request(request_url))
