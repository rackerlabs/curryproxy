import logging

import curryproxy.helpers as helpers
from curryproxy.errors import ConfigError
from .endpoints_route import EndpointsRoute
from .forwarding_route import ForwardingRoute
from .status_route import StatusRoute


def make(routeconfig):
    """Creates all routes defined in a configuration dictionary.

    Typically called using the dict returned by helpers.load or
    routes.config.load; either works.
    """

    if 'status' in routeconfig:
        # Note: there is only ever one status "route", consisting of a list
        # of urls.
        yield StatusRoute(routeconfig['status'])
    for pattern, dest in routeconfig.get('forwards', {}).items():
        yield ForwardingRoute(pattern, dest)
    for name, route in routeconfig.get('routes', {}).items():
        yield make_endpoint(name, route)


def make_endpoint(name, route):
    """ Create an endpoint route from a configuration entry

    name:   The route's name
    route:  The configuration dictionary for the route
    """
    # More complex. The config structure almost but doesn't quite match
    # the EndpointsRoute constructor, so a bit of massaging is needed
    # here. Some (all?) of this should probably be done in the
    # constructor instead, or maybe a from_dict classmethod.

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
