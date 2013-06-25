from testtools import TestCase

from curryproxy.routes import StatusRoute


class Test__Init__(TestCase):
    def test__url_patterns(self):
        url_patterns = ['https://1.example.com/status',
                        'https://2.example.com/status']

        status_route = StatusRoute(url_patterns)

        self.assertEqual(url_patterns, status_route._url_patterns)
