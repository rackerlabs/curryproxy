from errors import RouteError


class Route(object):
    def __init__(self, route_config):
        self._parse_dict(route_config)

    def _parse_dict(self, route_config):
        self._uri_pattern = None
        self._forwarding_uri = None
        self._endpoints = None

        if 'route' not in route_config:
            raise RouteError('Each route must contain "route"')
        self._uri_pattern = route_config['route']

        if ('forwarding_uri' in route_config and
                'endpoints' in route_config):
            raise RouteError('The route "{0}" cannot contain both '
                             '"forwarding_uri" and '
                             '"endpoints"'.format(self._uri_pattern))

        if 'forwarding_uri' in route_config:
            self._forwarding_uri = route_config['forwarding_uri']

        if 'endpoints' in route_config:
            if '{Endpoint_IDs}' not in self._uri_pattern:
                raise RouteError('The route "{0}" must contain the '
                                 'placeholder "{{Endpoint_IDs}}"'
                                 .format(self._uri_pattern))

            self._endpoints = {}
            for endpoint in route_config['endpoints']:
                self._endpoints[endpoint['id']] = endpoint['uri']

        if self._forwarding_uri is None and self._endpoints is None:
            raise RouteError('The route "{0}" must contain either '
                             '"forwarding_uri" or '
                             '"endpoints"'.format(self._uri_pattern))
