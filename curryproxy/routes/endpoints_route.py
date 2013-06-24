import logging
import re
import urllib

import grequests

from curryproxy.errors import ConfigError
from curryproxy.responses import ErrorResponse
from curryproxy.responses import MetadataResponse
from curryproxy.responses import MultipleResponse
from curryproxy.errors import RequestError
from curryproxy.routes.route_base import RouteBase
from curryproxy.responses import SingleResponse

from curryproxy.helpers import ENVIRON_REQUEST_UUID_KEY


ENDPOINTS_WILDCARD = '{Endpoint_IDs}'


class EndpointsRoute(RouteBase):
    def __init__(self, url_patterns, endpoints, priority_errors):
        self._url_patterns = url_patterns
        self._endpoints = {}
        self._priority_errors = priority_errors

        if '*' in endpoints:
            raise ConfigError('Asterisks are not permitted as endpoint IDs.')

        for endpoint_id in endpoints:
            lowered_endpoint_id = endpoint_id.lower()
            if lowered_endpoint_id in self._endpoints:
                raise ConfigError('Duplicate endpoint IDs for the same route '
                                  'are not permitted.')
            self._endpoints[lowered_endpoint_id] = endpoints[endpoint_id]

    def __call__(self, request):
        original_request = request.copy()

        destination_urls = self._create_forwarded_urls(request.url)

        # Use gzip even if the original requestor didn't support it
        request.headers['Accept-Encoding'] = 'gzip,identity'
        # Host header is automatically added for each request by grequests
        del request.headers['Host']

        requests = (grequests.request(request.method,
                                      destination_url,
                                      data=request.body,
                                      headers=request.headers,
                                      allow_redirects=False,
                                      verify=True)
                    for destination_url in destination_urls)
        requests_responses = grequests.map(requests, stream=True)

        response = None
        if None in requests_responses:
            response = MetadataResponse(original_request, requests_responses)
            response.response.status = 504
            request_uuid = original_request.environ[ENVIRON_REQUEST_UUID_KEY]
            logging.error('Unable to connect to one or more backend '
                          'endpoints: {0}'.format(', '.join(destination_urls)),
                          extra={'request_uuid': request_uuid})
        elif ('Proxy-Aggregator-Body' in original_request.headers
                and original_request.headers['Proxy-Aggregator-Body'].lower()
                == 'response-metadata'):
            response = MetadataResponse(original_request, requests_responses)
        elif len(requests_responses) == 1:
            response = SingleResponse(original_request, requests_responses[0])
        elif any(r.status_code >= 400 for r in requests_responses):
            response = ErrorResponse(original_request,
                                     requests_responses,
                                     self._priority_errors)
        else:
            response = MultipleResponse(original_request, requests_responses)

        return response.response

    def _create_forwarded_urls(self, request_url):
        # Extract endpoints from request
        url_pattern = self._find_pattern_for_request(request_url)
        url_pattern_parts = url_pattern.split(ENDPOINTS_WILDCARD)
        match_expression = re.escape(url_pattern_parts[0]) + \
            "(?P<endpoint_ids>.*)" + \
            re.escape(url_pattern_parts[1])
        endpoint_ids_group = re.match(match_expression,
                                      request_url).group("endpoint_ids")
        endpoint_ids = endpoint_ids_group.split(',')
        endpoint_ids = [urllib.unquote(e_id) for e_id in endpoint_ids]
        endpoint_ids = [e_id.strip().lower() for e_id in endpoint_ids]

        # Extract trailing portion of request URL
        trailing_route = request_url[len(url_pattern_parts[0]
                                         + endpoint_ids_group
                                         + url_pattern_parts[1]):]

        # Create final URLs to be forwarded
        endpoint_urls = []
        all_endpoints = False
        if '*' in endpoint_ids:
            all_endpoints = True

        for endpoint_id in self._endpoints:
            if all_endpoints or endpoint_id in endpoint_ids:
                url = self._endpoints[endpoint_id] + trailing_route
                endpoint_urls.append(url)

        if len(endpoint_urls) == 0:
            raise RequestError('The incoming request did not specify a valid '
                               'endpoint identifier for matched route: {0}'
                               .format(url_pattern))

        return endpoint_urls

    def _find_pattern_for_request(self, request_url):
        wildcard_escaped = re.escape(ENDPOINTS_WILDCARD)

        for url_pattern in self._url_patterns:
            pattern_escaped = re.escape(url_pattern)
            pattern_escaped = pattern_escaped.replace(wildcard_escaped,
                                                      '.*',
                                                      1)

            if re.match(pattern_escaped, request_url, re.IGNORECASE):
                return url_pattern

        return None
