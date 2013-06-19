from testtools import TestCase

from curryproxy.routes import EndpointsRoute


class Test_Create_Forwarded_Urls(TestCase):
    def setUp(self):
        super(Test_Create_Forwarded_Urls, self).setUp()

        url_patterns = ['https://example.com/{Endpoint_IDs}/',
                        'https://www.example.com/{Endpoint_IDs}/']
        self.endpoints = {"one": "https://1.example.com/",
                          "two": "https://2.example.com/"}
        self.route = EndpointsRoute(url_patterns, self.endpoints, [])

    def test_all_endpoints(self):
        request_path = 'path'
        request_url = 'https://example.com/*/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)

    def test_case_insensitivity(self):
        request_path = 'path'
        request_url = 'https://example.com/one,TwO/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)

    def test_single_endpoint(self):
        request_path = 'path'
        request_url = 'https://example.com/one/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        two_url = self.endpoints['two'] + request_path
        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(two_url not in forwarded_urls)

    def test_whitespace_encoded_leading(self):
        request_path = 'path'
        request_url = 'https://example.com/%20one,%20two/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)

    def test_whitespace_encoded_trailing(self):
        request_path = 'path'
        request_url = 'https://example.com/one%20,two%20/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)

    def test_whitespace_leading(self):
        request_path = 'path'
        request_url = 'https://example.com/ one, two/' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)

    def test_whitespace_trailing(self):
        request_path = 'path'
        request_url = 'https://example.com/one ,two /' + request_path

        forwarded_urls = self.route._create_forwarded_urls(request_url)

        self.assertTrue(self.endpoints['one'] + request_path in forwarded_urls)
        self.assertTrue(self.endpoints['two'] + request_path in forwarded_urls)
