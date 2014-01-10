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

        ignore_errors = set()
        if 'ignore_errors' in route_config:
            for entry in route_config['ignore_errors']:
                if entry.count('-') > 1:
                    raise ConfigError('The ignore error entry cannot contain multiple hyphens')
                elif entry.count('-') > 0:
                    start = entry.split('-')[0]
                    stop = entry.split('-')[1]

                    if '' in [start, stop]:
                        raise ConfigError('Ignore error ranges must include both starting and stopping values')

                    try:
                        start_num = int(start)
                        stop_num = int(stop)
                        
                        if start_num > stop_num:
                            raise ConfigError('The range beginning must be less than or equal to the range end')
                        if stop_num > 599:
                            raise ConfigError('Valid range values are between 0 and 599')

                        ignore_errors.update(range(start_num,stop_num+1))

                    except ValueError:
                        raise ConfigError('The ignore entry must be a valid numeric error code')
                else:
                    try:
                        ignore_errors.add(int(entry))
                    except ValueError:
                        raise ConfigError('The ignore entry must be a valid numeric error code')

        return EndpointsRoute(url_patterns, endpoints, priority_errors, list(ignore_errors))

    raise ConfigError('The route "{0}" must contain either "forwarding_url" '
                      'or "endpoints"'.format(url_patterns))
