from functools import partial

from testtools import TestCase
from mock import patch

from curryproxy import CurryProxy


class TestWsgi(TestCase):
    def setUp(self):
        super(TestWsgi, self).setUp()
        # curryproxy.wsgi uses the default conf file locations, which
        # are under /etc/curryproxy. That's not appropriate for tests,
        # so let's override them before importing.
        patched_cproxy = partial(CurryProxy, 'tests/etc')

        # Note that python caches curryproxy.wsgi here, so you can't get
        # the unpatched version of curryproxy.wsgi.app after this
        # without reload()ing it. That caused me some puzzlement.
        with patch("curryproxy.CurryProxy", patched_cproxy):
            import curryproxy.wsgi
            self.app = curryproxy.wsgi.app

    def test_wsgiapp(self):
        self.assertIsInstance(self.app, CurryProxy)
        self.assertEqual(3, len(self.app._routes))
