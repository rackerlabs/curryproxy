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
"""The classes in this module have been lifted into the package namespace.

Classes:
    EndpointsRoute: Handles forwarding a request to multiple backend endpoints.

Attributes:
    ENDPOINTS_WILDCARD: Wildcard which must be present in each URL pattern an
        EndpointsRoute can handle. The endpoints CurryProxy ultimately calls
        are determined by the endpoint IDs specified in place of the wildcard
        for a request.

"""
import logging
import re
import urllib

import grequests

from curryproxy.errors import ConfigError
from curryproxy.errors import RequestError
from curryproxy.helpers import ENVIRON_REQUEST_UUID_KEY
from curryproxy.responses import ErrorResponse
from curryproxy.responses import MetadataResponse
from curryproxy.responses import MultipleResponse
from curryproxy.responses import SingleResponse
from curryproxy.routes.route_base import RouteBase


ENDPOINTS_WILDCARD = '{Endpoint_IDs}'


class EndpointsRoute(RouteBase):
    """Handles forwarding a request to multiple backend endpoints.

    A request matched to this route will be forwarded to the configured
    endpoint with very little modification. The response received from the
    destination endpoint will be directly forwarded back to the client.

    """
    def __init__(self,
                 url_patterns,
                 endpoints,
                 priority_errors,
                 ignore_errors):
        """Initializes a new EndpointsRoute.

        Args:
            url_patterns: List of URL patterns which this route will handle.
                Incoming requests must begin with one of these patterns for
                this route to handle the request.
            endpoints: Dictionary mapping endpoint IDs to endpoint URLs.
                Endpoint IDs specified in incoming requests will be mapped to
                destination endpoints based on the values in this dictionary.
            priority_errors: List of error status codes, in order of
                precedence, to be immediately returned to the client if
                received from a destination endpoint.
            ignore_errors: List of error status codes or error status code
                ranges to exempt when checking response codes.  Format is
                ["400", "403-500"].

        Raises:
            ConfigError: An error was detected when parsing the data for this
                route.

        """
        self._url_patterns = url_patterns
        self._endpoints = {}
        self._priority_errors = priority_errors
        self._ignore_errors = ignore_errors

        if '*' in endpoints:
            raise ConfigError('Asterisks are not permitted as endpoint IDs.')

        for endpoint_id in endpoints:
            lowered_endpoint_id = endpoint_id.lower()
            if lowered_endpoint_id in self._endpoints:
                raise ConfigError('Duplicate endpoint IDs for the same route '
                                  'are not permitted.')
            self._endpoints[lowered_endpoint_id] = endpoints[endpoint_id]

    def __call__(self, request):
        requests_request = request.copy()

        destination_urls = self._create_forwarded_urls(requests_request.url)

        # Use gzip even if the original requestor didn't support it
        requests_request.headers['Accept-Encoding'] = 'gzip,identity'
        # Host header is automatically added for each request by grequests
        del requests_request.headers['Host']

        requests = (grequests.request(requests_request.method,
                                      destination_url,
                                      data=requests_request.body,
                                      headers=requests_request.headers,
                                      allow_redirects=False,
                                      verify=True)
                    for destination_url in destination_urls)
        requests_responses = grequests.map(requests, stream=True)

        requests_responses = self._filter_responses(requests_responses)

        response = None
        if None in requests_responses:
            response = MetadataResponse(request, requests_responses)
            response.response.status = 504
            request_uuid = request.environ[ENVIRON_REQUEST_UUID_KEY]
            logging.error('Unable to connect to one or more backend '
                          'endpoints: {0}'.format(', '.join(destination_urls)),
                          extra={'request_uuid': request_uuid})
        elif ('Proxy-Aggregator-Body' in request.headers
                and request.headers['Proxy-Aggregator-Body'].lower()
                == 'response-metadata'):
            response = MetadataResponse(request, requests_responses)
        elif len(requests_responses) == 1:
            response = SingleResponse(request, requests_responses[0])
        elif any(r.status_code >= 400 for r in requests_responses):
            response = ErrorResponse(request,
                                     requests_responses,
                                     self._priority_errors)
        else:
            response = MultipleResponse(request, requests_responses)

        return response.response

    def _filter_responses(self, responses):
        valid_responses = []
        for r in responses:
            if r is not None:
                if r.status_code not in self._ignore_errors:
                    valid_responses.append(r)
            elif 0 not in self._ignore_errors:
                valid_responses.append(r)
        if len(valid_responses) > 0:
            return valid_responses
        else:
            return responses

    def _create_forwarded_urls(self, request_url):
        """Constructs the destination endpoint(s) to request.

        Finds the matching URL pattern for the request_url. Once found, the
        final destination URLs are determined based on the endpoint IDs
        specified in the request in place of the wildcard section of the URL
        pattern. Finally, anything trailing the URL pattern is appended to each
        destination URL.

        Args:
            request_url: Incoming request URL from the client to be matched to
                a URL pattern and parsed to form the final destination URL(s).

        Returns:
            List of final destination URL(s) to which the incoming request
            should be forwarded.

        Raises:
            RequestError: The incoming request did not match any URL patterns
                for this route.

        """
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
