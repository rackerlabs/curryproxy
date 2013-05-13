from curry.errors import ConfigError
from curry.routes import EndpointsRoute
from curry.routes import ForwardingRoute


def parse_dict(route_config):
    url_patterns = None

    if 'route' not in route_config:
        raise ConfigError('Each route must contain "route"')
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

        return EndpointsRoute(url_patterns, endpoints)

    raise ConfigError('The route "{0}" must contain either "forwarding_url" '
                      'or "endpoints"'.format(url_patterns))
