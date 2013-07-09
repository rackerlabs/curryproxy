from testtools import ExpectedException, TestCase

from curryproxy import CurryProxy
from curryproxy.errors import ConfigError


class Test_Process_Routes(TestCase):
    def setUp(self):
        super(Test_Process_Routes, self).setUp()
        self.logging_conf_path = 'curryproxy/tests/etc/logging.console.conf'

    def test_config_invalid_json(self):
        with ExpectedException(ConfigError):
            CurryProxy('curryproxy/tests/etc/routes.invalid_json.json',
                       self.logging_conf_path)

    def test_config_invalid_path(self):
        with ExpectedException(IOError):
            CurryProxy('curryproxy/tests/etc/missing_file.json',
                       self.logging_conf_path)

    def test_config_valid(self):
        routes_path = 'curryproxy/tests/etc/routes.forwarding_address.json'
        curry = CurryProxy(routes_path, self.logging_conf_path)

        self.assertEqual(1, len(curry._routes))

    def test_config_multiple_routes(self):
        routes_path = 'curryproxy/tests/etc/routes.forwarding_addresses.json'
        curry = CurryProxy(routes_path, self.logging_conf_path)

        self.assertEqual(2, len(curry._routes))
