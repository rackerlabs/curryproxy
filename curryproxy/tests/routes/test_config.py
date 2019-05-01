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


class Test_Config_Version(testtools.TestCase):
    def test_confver_detection_v1(self):
        path = 'curryproxy/tests/etc/routes.v1.json'
        conf = helpers.load(path)
        self.assertEqual(1, config.version(conf))

    def test_confver_detection_v2(self):
        path = 'curryproxy/tests/etc/routes.v2.yaml'
        conf = helpers.load(path)
        self.assertEqual(2, config.version(conf))

    def test_confver_bogus_input(self):
        self.assertRaises(ConfigError, config.version, None)


class Test_Config_Normalize(testtools.TestCase):
    def test_config_normalize_v1(self):
        path = "curryproxy/tests/etc/routes.v{}.{}"
        v2yaml = config.normalize(helpers.load(path.format(2, "yaml")))
        v1yaml = config.normalize(helpers.load(path.format(1, "yaml")))
        v1json = config.normalize(helpers.load(path.format(1, "json")))

        # It's simpler to compare the re-serialization of the data
        # structures than the data structures themselves. Just have to
        # make sure dict key orders are sorted.

        def dump(data):  # Makes the comparisons easier to read
            return json.dumps(data, sort_keys=True)

        self.assertEqual(dump(v2yaml), dump(v1yaml))
        self.assertEqual(dump(v2yaml), dump(v1json))
