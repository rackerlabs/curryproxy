import testtools

from curryproxy.helpers import load
from curryproxy.errors import ConfigError


class Test_Load(testtools.TestCase):
    def setUp(self):
        super(Test_Load, self).setUp()
        self.etc = "tests/etc/"

    def test_format_yaml(self):
        path = self.etc + "routes.empty.yaml"
        self.assertEqual(load(path), {})

    def test_load_miss(self):
        path = self.etc + "missing_file.json"
        self.assertRaises(IOError, load, path)

    def test_bad_data(self):
        path = self.etc + "bad.yaml"
        self.assertRaises(ConfigError, load, path)
