import json

import testtools

import curryproxy
import curryproxy.helpers as helpers
import curryproxy.routes.config as config
from curryproxy.routes import StatusRoute
from curryproxy.routes import ForwardingRoute
from curryproxy.routes import EndpointsRoute
from curryproxy.routes import make
from curryproxy.routes import load
from curryproxy.errors import ConfigError

class Test_Config_Make(testtools.TestCase):
    def test_make_status_routes(self):
        path = 'curryproxy/tests/etc/routes.status.yaml'
        routes = list(make(load(path)))
        self.assertEqual(1, len(routes))
        self.assertIsInstance(routes[0], StatusRoute)

    def test_make_forwarding_routes(self):
        path = 'curryproxy/tests/etc/routes.forwarding_address.json'
        routes = list(make(load(path)))
        self.assertEqual(1, len(routes))
        self.assertIsInstance(routes[0], ForwardingRoute)

    def test_make_endpoint_routes(self):
        path = 'curryproxy/tests/etc/routes.endpoints.yaml'
        routes = list(make(load(path)))
        self.assertEqual(2, len(routes))
        self.assertIsInstance(routes[0], EndpointsRoute)

    def test_make_multiple_routes(self):
        path = 'curryproxy/tests/etc/routes.v2.yaml'
        routes = list(make(load(path)))
        self.assertEqual(3, len(routes))

    def test_endpoint_invalid_erange(self):
        # Take a valid conf and munge error lists a few different ways.
        path = 'curryproxy/tests/etc/routes.v2.yaml'
        config = load(path)
        for erange in [50, "50", "40-300", "300-1000"]:
            config['routes']['route1']['ignore_errors'] = [erange]
            self.assertRaises(ConfigError, list, make(config))

    def test_endpoint_missing_errange(self):
        path = 'curryproxy/tests/etc/routes.endpoints.yaml'
        conf = load(path)
        name = 'noerrors'
        route = config.make_endpoint(name, conf['routes'][name])
        self.assertEquals([], route._priority_errors)
        self.assertEquals([], route._ignore_errors)


class Test_Config_Load(testtools.TestCase):
    def test_broken_config(self):
        path = 'curryproxy/tests/etc/routes.invalid_json.json'
        self.assertRaises(ConfigError, config.load, path)
