import re
from urlparse import urlparse

import requests
from webob import Response

from curry.errors import RequestError
from curry.routes.route_base import RouteBase


class ForwardingRoute(RouteBase):
    def __init__(self, url_patterns, forwarding_url):
        self._url_patterns = url_patterns
        self._forwarding_url = forwarding_url

    def match(self, request_url):
        if self._find_pattern_for_request(request_url) is not None:
            return True

        return False

    def _find_pattern_for_request(self, request_url):
        for url_pattern in self._url_patterns:
            url_pattern_escaped = re.escape(url_pattern)

            if re.match(url_pattern_escaped, request_url, re.IGNORECASE):
                return url_pattern

        return None

    def issue_request(self, request):
        destination_url = self._create_forwarded_url(request.url)
        request.headers['Host'] = urlparse(destination_url).netloc

        requests_response = requests.request(request.method,
                                             destination_url,
                                             data=request.body,
                                             headers=request.headers,
                                             allow_redirects=False,
                                             verify=True)

        webob_response = Response()
        webob_response.status = requests_response.status_code
        webob_response.headers = requests_response.headers
        webob_response.body = requests_response.content

        return webob_response

    def _create_forwarded_url(self, request_url):
        url_pattern = self._find_pattern_for_request(request_url)
        url_pattern_escaped = re.escape(url_pattern)

        forwarded_url, count = re.subn(url_pattern_escaped,
                                       self._forwarding_url,
                                       request_url,
                                       1,
                                       re.IGNORECASE)

        if count != 1:
            raise RequestError('Provided request_url did not match the route '
                               '{0}'.format(self._url_pattern))

        return forwarded_url
