import testtools

from curryproxy.curryproxy import CurryProxy


class Test___Init__(testtools.TestCase):
    def test_config_default(self):
        try:
            CurryProxy()
        except IOError:
            self.fail('Requires the default /etc/curry/routes.json file to '
                      'be present & valid.')

    def test_config_supplied(self):
        curry = CurryProxy('curryproxy/tests/etc/routes.forwarding_address.json')

        self.assertEqual(1, len(curry._routes))
