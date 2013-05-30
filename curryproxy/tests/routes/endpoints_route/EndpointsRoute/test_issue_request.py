import sys

from testtools import ExpectedException
from mock import Mock
from webob import Request
from testtools import TestCase

from curryproxy.routes import EndpointsRoute


class TestIssue_Request(TestCase):
    def test_requests_streamed(self):
        url_patterns = ['http://example.com/{Endpoint_IDs}/']
        endpoints = {'test': 'http://example.com/'}
        route = EndpointsRoute(url_patterns, endpoints)

        request = Request.blank('http://example.com/test/path')

        # TODO: Convert this to use mock.patch
        grequests_map = sys.modules['grequests'].map
        sys.modules['grequests'].map = Mock()

        with ExpectedException(TypeError):
            route.issue_request(request)

        self.assertTrue({'stream': True} in
                        sys.modules['grequests'].map.call_args)

        sys.modules['grequests'].map = grequests_map
