from testtools import ExpectedException
from testtools import TestCase

from curryproxy.tests.routes.route_base.RouteBase import RouteBaseTest


class Test_Find_Pattern_For_Request(TestCase):
    def test_abstractmethod(self):
        route_base = RouteBaseTest()

        with ExpectedException(NotImplementedError):
            route_base._find_pattern_for_request(None)
