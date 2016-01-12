# Copyright (c) 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Produces routes based on information found in a configuration file.

Functions:
    parse_dict: Produces a route based on an entry in CurryProxy's
        configuration file.
    parse_ignore_rules: Parses CurryProxy's configuration file for
        rules defining return codes that may be bypassed.

"""
import itertools
import collections

from curryproxy.errors import ConfigError
from curryproxy.routes import EndpointsRoute
from curryproxy.routes import ForwardingRoute
from curryproxy.routes import StatusRoute

CONF_LATEST_VERSION = 2


def parse_ignore_rules(route_config):
    ignore_errors = set()
    if 'ignore_errors' in route_config:
        for entry in route_config['ignore_errors']:
            hyphens = entry.count('-')
            try:
                if hyphens > 1:
                    # Malformed
                    raise ValueError
                elif hyphens > 0:
                    # Add range rule
                    [start, stop] = map(int, entry.split('-'))
                else:
                    # Add single rule
                    start = int(entry)
                    stop = start
            except ValueError:
                raise ConfigError('Rules must be numbers in the format '
                                  'of "400" or "400-500"')
            if stop > 599:
                raise ConfigError('Error status is constrained to the '
                                  'range 100 - 599')
            if start > stop:
                raise ConfigError('Start value of a range must be less '
                                  'than or equal to the stop value')
            ignore_errors.update(range(start, stop + 1))
    return ignore_errors


def load(route_configs):
    """Creates all routes defined in a configuration file.

    This function is version-agnostic and will do any conversions necessary to
    load old versions of the configuration format. It expects a data structure
    read in from a configuration file with json.load, yaml.load, or similar.
    """
    # I'm not sure how the route objects this returns get used by the program;
    # would it be useful/desirable to return a (statusroutes, forwards,
    # endpoints) tuple instead?
    return list(_load(_convert(route_configs)))


def _load(route_configs):
    """Generates all routes in a configuration file.

    This function creates Route objects based on the most recent config file
    format, i.e. it expects _convert to already have been called.
    """
    assert route_configs['configVersion'] == CONF_LATEST_VERSION

    for s in route_configs.get('status', []):
        yield StatusRoute(s)

    for src, dest in route_configs.get('forwards', {}).items():
        yield ForwardingRoute(src, dest)

    for d in route_configs.get('routes', {}):
        # Config v2 almost but doesn't quite match the EndpointsRoute
        # constructor, so a bit of massaging is needed here...
        d = d.copy()

        # Convert error ranges into discrete lists.
        ignore = []
        for e in d['ignore_errors']:
            e = str(e)
            r = e.split("-")
            start, end = int(r[0]), int(r[-1])
            ignore.extend(range(start, end+1))
        d['ignore_errors'] = ignore

        # Accept singular url_pattern or plural url_patterns.
        patterns = d.get('url_patterns', [])
        if 'url_pattern' in d:
            patterns.append(d.pop('url_pattern'))
        d['url_patterns'] = patterns

        yield EndpointsRoute(**d)


def _convert(route_configs):
    """Update old configuration data structure versions.

    Returns a new data structure of the current version.

    Should this be public?"""
    # Convert from each version to the next version and repeat until reaching
    # the latest. This makes it so we don't have to re-write the conversion
    # code for all versions any time the configuration format changes; we only
    # need to add a new function for the immediate prior version.

    # First figure out what version we're working with.
    try:
        version = route_configs['configVersion']
    except (TypeError):
        # Version 1 had no specifier, but we can identify it anyway because its
        # root node was not a dict.
        version = 1
    except (KeyError):
        # If configVersion isn't provided, complain. Ideally this should
        # autodetect in future.
        raise ConfigError("configVersion format identifier missing.")

    # Get the conversion functions between `version` and the current one, then
    # call them sequentially. This relies on them all being named
    # `_convert_v(number)`
    converters = [globals()["_convert_v{}".format(i)]
                  for i in range(version, CONF_LATEST_VERSION)]
    for nextver in converters:
        route_configs = nextver(route_configs)
    return route_configs


def _convert_v1(route_configs):
    """Convert a v1 configuration data structure to v2."""

    # Config version 1 was a top level list containing dicts that had a
    # type marker. It was the only version without a version specifier.
    newconf = dict()
    newconf['configVersion'] = 2

    # Status routes require no changes other than being moved to the top level.
    # This will accept (and concatenate) multiple status-route dicts in the
    # source, although it doesn't look like that was ever intended.
    statusroutes = [d['status'] for d
                    in route_configs
                    if 'status' in d]
    newconf['status'] = list(itertools.chain.from_iterable(statusroutes))

    # Forwards were changed from key-value pairs mixed in with other stuff to a
    # flat dict.
    newconf['forwards'] = {d['route']: d['forwarding_url']
                           for d in route_configs
                           if 'forwarding_url' in d}

    # Endpoint routes had one key renamed to match the EPR constructor, and the
    # endpoints subdict was changed from a list of key-value dicts to a flat
    # dict (which also matches the constructor). It's cleaner here to build the
    # list first and modify it afterward.
    newconf['routes'] = [d for d in route_configs
                         if 'endpoints' in d]

    for ep in newconf['routes']:
        ep['url_patterns'] = [ep.pop('route')]
        ep['endpoints'] = {ep['id']: ep['url'] for ep in ep['endpoints']}

    return newconf


def parse_dict(route_config):
    """Produces a route based on an entry in CurryProxy's configuration file.

    Note that this function will be called multiple times, once for each route
    CurryProxy is configured to handle.

    Args:
        route_config: Dictionary representing one entry in CurryProxy's
            configuration file.

    Raises:
        ConfigError: An error was detected when parsing the data found in the
            configuration file.

    """
    url_patterns = None

    if 'status' in route_config:
        return StatusRoute(route_config['status'])

    if 'route' not in route_config:
        raise ConfigError('Each route must contain "route"')
    # Convert to list for later support of multiple routes per endpoint
    url_patterns = [route_config['route']]

    if ('forwarding_url' in route_config and
            'endpoints' in route_config):
        raise ConfigError('The route "{0}" cannot contain both '
                          '"forwarding_url" and "endpoints"'
                          .format(url_patterns))

    if 'forwarding_url' in route_config:
        return ForwardingRoute(url_patterns, route_config['forwarding_url'])

    if 'endpoints' in route_config:
        if any('{Endpoint_IDs' not in pattern for pattern in url_patterns):
            raise ConfigError('The route "{0}" must contain the '
                              'placeholder "{{Endpoint_IDs}}"'
                              .format(url_patterns))

        endpoints = {}
        for endpoint in route_config['endpoints']:
            endpoints[endpoint['id']] = endpoint['url']

        priority_errors = []
        if 'priority_errors' in route_config:
            priority_errors = route_config['priority_errors']

        ignore_errors = parse_ignore_rules(route_config)

        return EndpointsRoute(url_patterns,
                              endpoints,
                              priority_errors,
                              list(ignore_errors))

    raise ConfigError('The route "{0}" must contain either "forwarding_url" '
                      'or "endpoints"'.format(url_patterns))
