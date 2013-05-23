from testtools import ExpectedException, TestCase

from curryproxy.curryproxy import CurryProxy
from curryproxy.errors import ConfigError


class Test_Process_Routes(TestCase):
    def test_config_invalid_json(self):
        with ExpectedException(ConfigError):
            CurryProxy('curryproxy/tests/etc/routes.invalid_json.json')

    def test_config_invalid_path(self):
        with ExpectedException(IOError):
            CurryProxy('curryproxy/tests/etc/missing_file.json')

    def test_config_valid(self):
        curry = CurryProxy('curryproxy/tests/etc/routes.forwarding_address.json')

        self.assertEqual(1, len(curry._routes))

    def test_config_multiple_routes(self):
        curry = CurryProxy('curryproxy/tests/etc/routes.forwarding_addresses.json')

        self.assertEqual(2, len(curry._routes))
