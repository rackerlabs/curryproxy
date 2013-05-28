from mock import Mock
import testtools

from curryproxy.curryproxy import CurryProxy


class Test___Init__(testtools.TestCase):
    def test_config_default(self):
        old_method = CurryProxy._process_routes
        CurryProxy._process_routes = Mock()

        CurryProxy()

        default_path = '/etc/curryproxy/routes.json'
        CurryProxy._process_routes.assert_called_with(default_path)

        CurryProxy._process_routes = old_method

    def test_config_supplied(self):
        route_file_path = 'curryproxy/tests/etc/routes.forwarding_address.json'
        curry = CurryProxy(route_file_path)

        self.assertEqual(1, len(curry._routes))
