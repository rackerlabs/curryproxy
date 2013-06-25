import re
from urlparse import urlparse

import requests

from curryproxy.errors import RequestError
from curryproxy.routes.route_base import RouteBase
from curryproxy.responses import SingleResponse


class ForwardingRoute(RouteBase):
    def __init__(self, url_patterns, forwarding_url):
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
        url_pattern = self._find_pattern_for_request(request_url)
        if not url_pattern:
            raise RequestError('Requested URL "{0}" did not match the '
                               'forwarding route "{1}"'
                               .format(request_url,
                                       ', '.join(self._url_patterns)))

        url_pattern_escaped = re.escape(url_pattern)

        forwarded_url, count = re.subn(url_pattern_escaped,
                                       self._forwarding_url,
                                       request_url,
                                       1,
                                       re.IGNORECASE)

        return forwarded_url

    def _find_pattern_for_request(self, request_url):
        for url_pattern in self._url_patterns:
            url_pattern_escaped = re.escape(url_pattern)

            if re.match(url_pattern_escaped, request_url, re.IGNORECASE):
                return url_pattern

        return None
