from webob import Request
from testtools import TestCase

from curryproxy.routes import StatusRoute


class Test__Call__(TestCase):
    def test_response(self):
        status_url = 'https://www.example.com/status'
        url_patterns = [status_url]

        status_route = StatusRoute(url_patterns)
        response = status_route(Request.blank(status_url))

        self.assertEqual('200 OK', response.status)
        self.assertTrue('hostname' in response.json)
