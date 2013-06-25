from testtools import ExpectedException
from testtools import TestCase

from curryproxy.tests.routes.route_base.RouteBase import RouteBaseTest


class Test__Call__(TestCase):
    def test_abstractmethod(self):
        route_base = RouteBaseTest()

        with ExpectedException(NotImplementedError):
            route_base(None)
