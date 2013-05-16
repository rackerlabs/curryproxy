from testtools import ExpectedException, TestCase

from curry.curry import Curry
from curry.errors import ConfigError


class TestCurryCurry_Process_Routes(TestCase):
    def test_config_invalid_json(self):
        with ExpectedException(ConfigError):
            Curry('curry/tests/etc/routes.invalid_json.json')

    def test_config_invalid_path(self):
        with ExpectedException(IOError):
            Curry('curry/tests/etc/missing_file.json')

    def test_config_valid(self):
        curry = Curry('curry/tests/etc/routes.forwarding_address.json')

        self.assertEqual(1, len(curry._routes))

    def test_config_multiple_routes(self):
        curry = Curry('curry/tests/etc/routes.forwarding_addresses.json')

        self.assertEqual(2, len(curry._routes))
