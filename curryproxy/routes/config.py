import itertools
import logging

import curryproxy.helpers as helpers
from curryproxy.errors import ConfigError
from .endpoints_route import EndpointsRoute
from .forwarding_route import ForwardingRoute
from .status_route import StatusRoute

CONF_LATEST_VERSION = 2


def load(filename):
    """ Load route configuration from a given filename.

    Returns a dictionary with top level keys for "status", "forwards",
    and "routes".
    """
    logging.debug("Loading conf file from %s", filename)
    conf = helpers.load(filename)
    logging.debug("Normalizing conf file")
    conf = normalize(conf)
    return conf


def make(routeconfig):
    """Creates all routes defined in a configuration dictionary.

    Typically called using the dict returned by helpers.load or
    routes.config.load; either works.
    """

    routeconfig = normalize(routeconfig)  # Just in case

    if 'status' in routeconfig:
        yield make_status(routeconfig['status'])
    for pattern, dest in routeconfig.get('forwards', {}).items():
        yield make_forward(pattern, dest)
    for name, route in routeconfig.get('routes', {}).items():
        yield make_endpoint(name, route)


def make_status(urls):
    """ Create a status route from configuration

    urls: the list of URLs under the `status` conf section.
    """
    # Note: there is only ever one status "route", consisting of a list
    # of urls.
    logging.debug("constructing status route")
    for i, url in enumerate(urls):
        logging.debug("status url %s: %s", i, url)
    return StatusRoute(urls)


def make_forward(pattern, dest):
    """ Create a forwarding route from a configuration entry

    `pattern` and `dest` are the key and value from the `forwards` conf
    section, respectively.
    """

    # For some reason, the conf files supply a single forwarding URL
    # but the ForwardingRoute constructor expects a list. Give it
    # what it wants.
    logging.debug("constructing forwarding route: %s -> %s", pattern, dest)
    return ForwardingRoute([pattern], dest)


def make_endpoint(name, route):
    """ Create an endpoint route from a configuration entry

    name:   The route's name
    route:  The configuration dictionary for the route
    """
    # More complex. The config structure almost but doesn't quite match
    # the EndpointsRoute constructor, so a bit of massaging is needed
    # here. Some (all?) of this should probably be done in the
    # constructor instead.

    logging.debug("constructing normal route: %s", name)

    # Work on a copy in case the caller is doing anything else with the
    # argument.
    route = route.copy()

    # Empty defaults for ignore/prioritize errors
    for elist in 'ignore_errors', 'priority_errors':
        if elist not in route:
            route[elist] = []

    # Convert error ranges into discrete lists.
    ignore = []
    for s in route.get('ignore_errors', []):
        ignore.extend(helpers.intrange(s))
    route['ignore_errors'] = ignore

    # Check that ignored/prioritized error numbers are valid.
    msg = "Rule {} {} error {}, but it is outside the valid range ({}-{})"
    errs = [("ignores",     route['ignore_errors']),
            ("prioritizes", route['priority_errors'])]
    emin = 100
    emax = 599
    for verb, errors in errs:
        for e in errors:
            if not (emin <= e <= emax):
                raise ConfigError(msg.format(name, verb, e, emin, emax))

    # Accept patterns as a list or as a single item, for convenience.
    # The route constructor accepts a list only.
    patterns = route.pop('patterns', [])
    if 'pattern' in route:
        patterns.append(route.pop('pattern'))
    route['url_patterns'] = patterns

    # Our dict now matches the constructor's expected args, so splat it in.
    return EndpointsRoute(**route)


def version(routes_config):
    """Detect a configuration structure's schema version.

    Used for backwards compatibility. Returns an integer.
    """
    if isinstance(routes_config, list):
        return 1
    elif isinstance(routes_config, dict):
        return 2
    else:
        msg = "Invalid config structure: {}"
        raise ConfigError(msg.format(routes_config))


def normalize(routes_config):
    """ Update configuration data using the old schema.

    Returns a new data structure with the current schema.
    """

    # Convert from each version to the next version and repeat until reaching
    # the latest. This makes it so we don't have to re-write the conversion
    # code for all versions any time the configuration format changes; we only
    # need to add a new function for the immediate prior version.
    converters = [globals()["_convert_v{}".format(i)]
                  for i in range(version(routes_config), CONF_LATEST_VERSION)]
    for nextver in converters:
        routes_config = nextver(routes_config)
    return routes_config


def _convert_v1(routes_config):
    """Convert a v1 configuration data structure to v2."""

    # Config version 1 was a top level list containing dicts that had a
    # type marker.
    newconf = dict()

    # Status routes require no changes other than being moved to the top level.
    # This will accept (and concatenate) multiple status-route dicts in the
    # source, although it doesn't look like that was ever intended.
    statusroutes = [d['status'] for d
                    in routes_config
                    if 'status' in d]
    if statusroutes:
        newconf['status'] = list(itertools.chain.from_iterable(statusroutes))

    # Forwards were changed from key-value pairs mixed in with other stuff to a
    # flat dict.
    newconf['forwards'] = {d['route']: d['forwarding_url']
                           for d in routes_config
                           if 'forwarding_url' in d}

    # The endpoint route changes are a bit more complex. It's cleaner here to
    # build the list first and modify it afterward.
    #
    # The new routes structure became a dict where the key is the route's
    # "name". The old conf file had no route names, so we'll use the generic
    # "routeN"

    endpoint_routes = [r for r in routes_config
                       if 'endpoints' in r]
    newconf['routes'] = {"route{}".format(i): d
                         for i, d in enumerate(endpoint_routes, 1)}

    for route in newconf['routes'].itervalues():
        # The old "route" key was renamed "pattern"
        route['pattern'] = [route.pop('route')]
        # The endpoint substructure was flattened into a dictionary.
        route['endpoints'] = {ep['id']: ep['url']
                              for ep in route['endpoints']}
    return newconf
