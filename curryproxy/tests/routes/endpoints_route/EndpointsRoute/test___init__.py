from testtools import ExpectedException
from testtools import TestCase

from curryproxy.errors import ConfigError
from curryproxy.routes import EndpointsRoute


class Test__Init__(TestCase):
    def test_duplicate_endpoint_ids(self):
        endpoints = {"one": "http://1.example.com/",
                     "ONE": "http://1.example.com/",
                     "two": "http://2.example.com/"}

        with ExpectedException(ConfigError):
            EndpointsRoute(None, endpoints, None)

    def test_endpoint_ids_lowered(self):
        endpoints = {"ONE": "http://1.example.com/",
                     "two": "http://2.example.com/"}

        endpoints_route = EndpointsRoute(None, endpoints, None)

        self.assertTrue('one' in endpoints_route._endpoints)
        self.assertFalse('ONE' in endpoints_route._endpoints)

    def test_forbidden_endpoint_id_asterisk(self):
        endpoints = {"one": "http://1.example.com/",
                     "*": "http://2.example.com/"}

        with ExpectedException(ConfigError):
            EndpointsRoute(None, endpoints, None)
