from testtools import TestCase

from curryproxy.routes import EndpointsRoute


class Test_Find_Pattern_For_Request(TestCase):
    def setUp(self):
        super(Test_Find_Pattern_For_Request, self).setUp()

        self.url_patterns = ['https://example.com/{Endpoint_IDs}/',
                             'https://www.example.com/{Endpoint_IDs}/']
        endpoints = {"ONE": "https://1.example.com/",
                     "two": "https://2.example.com/"}
        self.route = EndpointsRoute(self.url_patterns, endpoints, [])

    def test_whitespace_encoded_leading(self):
        request_url = 'https://example.com/%20ONE,%20two/path'

        url_pattern = self.route._find_pattern_for_request(request_url)

        self.assertEquals(self.url_patterns[0], url_pattern)

    def test_whitespace_encoded_trailing(self):
        request_url = 'https://example.com/ONE%20,two%20/path'

        url_pattern = self.route._find_pattern_for_request(request_url)

        self.assertEquals(self.url_patterns[0], url_pattern)

    def test_whitespace_leading(self):
        request_url = 'https://example.com/ ONE, two/path'

        url_pattern = self.route._find_pattern_for_request(request_url)

        self.assertEquals(self.url_patterns[0], url_pattern)

    def test_whitespace_trailing(self):
        request_url = 'https://example.com/ONE ,two /path'

        url_pattern = self.route._find_pattern_for_request(request_url)

        self.assertEquals(self.url_patterns[0], url_pattern)
