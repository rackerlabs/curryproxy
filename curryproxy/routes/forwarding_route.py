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
    ForwardingRoute: Direct communication with a single endpoint.

"""
import re
from urlparse import urlparse

import requests

from curryproxy.errors import RequestError
from curryproxy.responses import SingleResponse
from curryproxy.routes.route_base import RouteBase


class ForwardingRoute(RouteBase):
    """Direct communication with a single endpoint.

    A request matched to this route will be forwarded to the configured
    endpoint with very little modification. The response received from the
    destination endpoint will be directly forwarded back to the client.

    """
    def __init__(self, url_patterns, forwarding_url):
        """Initialize a new ForwardingRoute.

        Args:
            url_patterns: List of URL patterns which this route will handle.
                Incoming requests must begin with one of these patterns for
                this route to handle the request.
            forwarding_url: Destination endpoint the request will be forwarded
                to. Any portion of the incoming request URL following the
                matched URL pattern will be appended to forwarding_url to
                construct the final URL to request.

        """
        self._url_patterns = url_patterns
        self._forwarding_url = forwarding_url

    def __call__(self, request):
        requests_request = request.copy()

        destination_url = self._create_forwarded_url(requests_request.url)
        # Take advantage of gzip even if the client doesn't support it
        requests_request.headers['Accept-Encoding'] = 'gzip,identity'
        requests_request.headers['Host'] = urlparse(destination_url).netloc

        requests_response = requests.request(requests_request.method,
                                             destination_url,
                                             data=requests_request.body,
                                             headers=requests_request.headers,
                                             allow_redirects=False,
                                             verify=True,
                                             stream=True)

        single_response = SingleResponse(request, requests_response)
        return single_response.response

    def _create_forwarded_url(self, request_url):
        """Constructs a destination endpoint to request.

        Finds the matching URL pattern for the request_url. Anything trailing
        the pattern is appended to _forwarding_url to construct the final
        destination URL.

        Args:
            request_url: Incoming request URL from the client to be matched to
                a URL pattern and parsed to form the final destination URL.

        Returns:
            Final destination URL to which the incoming request should be
            forwarded.

        Raises:
            RequestError: The incoming request did not match any URL patterns
                for this route.

        """
        url_pattern = self._find_pattern_for_request(request_url)
        if not url_pattern:
            raise RequestError('Requested URL "{0}" did not match the '
                               'forwarding route "{1}"'
                               .format(request_url,
                                       ', '.join(self._url_patterns)))

        url_pattern_escaped = re.escape(url_pattern)

        forwarded_url = re.subn(url_pattern_escaped,
                                self._forwarding_url,
                                request_url,
                                1,
                                re.IGNORECASE)

        return forwarded_url[0]

    def _find_pattern_for_request(self, request_url):
        for url_pattern in self._url_patterns:
            url_pattern_escaped = re.escape(url_pattern)

            if re.match(url_pattern_escaped, request_url, re.IGNORECASE):
                return url_pattern

        return None
