import re

from errors import ConfigError, RequestError


class Route(object):
    def __init__(self, route_config):
        self._parse_dict(route_config)

    def _parse_dict(self, route_config):
        self._url_pattern = None
        self._forwarding_url = None
        self._endpoints = None

        if 'route' not in route_config:
            raise ConfigError('Each route must contain "route"')
        self._url_pattern = route_config['route']

        if ('forwarding_url' in route_config and
                'endpoints' in route_config):
            raise ConfigError('The route "{0}" cannot contain both '
                              '"forwarding_url" and '
                              '"endpoints"'.format(self._url_pattern))

        if 'forwarding_url' in route_config:
            self._forwarding_url = route_config['forwarding_url']

        if 'endpoints' in route_config:
            if '{Endpoint_IDs}' not in self._url_pattern:
                raise ConfigError('The route "{0}" must contain the '
                                  'placeholder "{{Endpoint_IDs}}"'
                                  .format(self._url_pattern))

            self._endpoints = {}
            for endpoint in route_config['endpoints']:
                self._endpoints[endpoint['id']] = endpoint['url']

        if self._forwarding_url is None and self._endpoints is None:
            raise ConfigError('The route "{0}" must contain either '
                              '"forwarding_url" or '
                              '"endpoints"'.format(self._url_pattern))

    def match(self, request_url):
        url_pattern_escaped = re.escape(self._url_pattern)

        if re.match(url_pattern_escaped, request_url, re.IGNORECASE):
            return True
        else:
            return False

    def create_forwarded_url(self, request_url):
        url_pattern_escaped = re.escape(self._url_pattern)

        forwarded_url, count = re.subn(url_pattern_escaped,
                                       self._forwarding_url,
                                       request_url,
                                       1,
                                       re.IGNORECASE)

        if count != 1:
            raise RequestError('Provided request_url did not match the route '
                               '{0}'.format(self._url_pattern))

        return forwarded_url
