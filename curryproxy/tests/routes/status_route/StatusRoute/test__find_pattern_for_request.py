from testtools import TestCase

from curryproxy.routes import StatusRoute


class Test_Find_Pattern_For_Request(TestCase):
    def setUp(self):
        super(Test_Find_Pattern_For_Request, self).setUp()

        self.url_patterns = ['https://www.example.com/status']

    def test_request_url_matched(self):
        status_route = StatusRoute(self.url_patterns)

        request_url = 'https://www.example.com/status'
        found_pattern = status_route._find_pattern_for_request(request_url)

        self.assertTrue(found_pattern)

    def test_request_url_unmatched(self):
        status_route = StatusRoute(self.url_patterns)

        request_url = 'https://www.example.com/status2'
        found_pattern = status_route._find_pattern_for_request(request_url)

        self.assertEqual(None, found_pattern)
