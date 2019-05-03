import logging

from testtools import TestCase
from mock import patch

from curryproxy.helpers import init_log
from curryproxy.errors import ConfigError


class Test_Init_Log(TestCase):
    def setUp(self):
        super(Test_Init_Log, self).setUp()
        self.etc = "curryproxy/tests/etc/"

    def test_logconf(self):
        self.skipTest("No test for logconf load yet")

    def test_missing_logconf(self):
        self.skipTest("no test for missing logconf yet")


    def test_malformed_logconf(self):
        path = self.etc + "bad.yaml"
        self.assertRaises(ConfigError, init_log, path)
