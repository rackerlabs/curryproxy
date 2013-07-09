from mock import patch
import testtools

from curryproxy import CurryProxy


class Test___Init__(testtools.TestCase):
    def setUp(self):
        super(Test___Init__, self).setUp()
        self.patcher = patch('logging.config')
        self.patcher.start()

    def test_config_default(self):
        patch_path = 'curryproxy.CurryProxy._process_routes'
        with patch(patch_path) as mocked_method:
            CurryProxy()

            default_path = '/etc/curryproxy/routes.json'
            mocked_method.assert_called_with(default_path)

    def test_config_supplied(self):
        route_file_path = 'curryproxy/tests/etc/routes.forwarding_address.json'
        curry = CurryProxy(route_file_path)

        self.assertEqual(1, len(curry._routes))

    def tearDown(self):
        super(Test___Init__, self).tearDown()
        self.patcher.stop()
