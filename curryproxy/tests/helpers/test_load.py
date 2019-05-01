import logging
from ConfigParser import ConfigParser

import testtools
from mock import patch

from curryproxy.helpers import load
from curryproxy.errors import ConfigError


class Test_Load(testtools.TestCase):
    def setUp(self):
        super(Test_Load, self).setUp()
        self.etc = "curryproxy/tests/etc/"

    def test_format_yaml(self):
        path = self.etc + "routes.empty.yaml"
        self.assertEqual(load(path), {})

    def test_format_json(self):
        path = self.etc + "routes.empty.json"
        self.assertEqual(load(path), [])

    def test_format_cparser(self):
        path = self.etc + "test.ini"
        cp = load(path)
        self.assertIsInstance(cp, ConfigParser)
        self.assertEqual(cp.get("section1", "key"), "value")

    def test_format_logconf(self):
        path = self.etc + "logging.conf"
        with patch("logging.config.fileConfig") as fileConfig:
            load(path)
            log = logging.getLogger("curry.conftest")
            self.assertIsInstance(log.handlers[0], logging.NullHandler)



    def test_load_miss(self):
        path = self.etc + "missing_file.json"
        self.assertRaises(IOError, load, path)

    def test_search_miss(self):
        path = self.etc
        self.assertRaises(IOError, load.search, "missing_file", self.etc)

    def test_invalid_data(self):
        path = self.etc + "routes.invalid_json.json"
        self.assertRaises(ConfigError, load, path)

    def test_unknown_filetype(self):
        self.assertRaises(ValueError, load, "routes.invalid")
