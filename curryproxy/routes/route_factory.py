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

"""
from curryproxy.errors import ConfigError
from curryproxy.routes import EndpointsRoute
from curryproxy.routes import ForwardingRoute
from curryproxy.routes import StatusRoute


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

        return EndpointsRoute(url_patterns, endpoints, priority_errors)

    raise ConfigError('The route "{0}" must contain either "forwarding_url" '
                      'or "endpoints"'.format(url_patterns))
