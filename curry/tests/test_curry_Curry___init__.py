import testtools

from curry.curry import Curry


class TestCurryCurry___init__(testtools.TestCase):
    def test_config_default(self):
        try:
            Curry()
        except IOError:
            self.fail('Requires the default /etc/curry/routes.json file to '
                      'be present & valid.')

    def test_config_supplied(self):
        curry = Curry('curry/tests/etc/routes.forwarding_address.json')

        self.assertEqual(1, len(curry._routes))
