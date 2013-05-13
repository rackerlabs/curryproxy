import json
import re
from urlparse import urlparse

from webob import Response
import requests

from curry.errors import RequestError
from curry.routes.route_base import RouteBase


ENDPOINTS_WILDCARD = '{Endpoint_IDs}'


class EndpointsRoute(RouteBase):
    def __init__(self, url_patterns, endpoints):
        self._url_patterns = url_patterns
        self._endpoints = endpoints

    def match(self, request_url):
        if self._find_pattern_for_request(request_url) is not None:
            return True

        return False

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

    def issue_request(self, request):
        destination_urls = self._create_forwarded_urls(request.url)

        requests_responses = []
        for destination_url in destination_urls:
            request.headers['Host'] = urlparse(destination_url).netloc

            requests_response = requests.request(request.method,
                                                 destination_url,
                                                 data=request.body,
                                                 headers=request.headers,
                                                 allow_redirects=False,
                                                 verify=True)
            requests_responses.append(requests_response)

        webob_response = Response()
        webob_response.status = requests_responses[0].status_code
        webob_response.headers = requests_responses[0].headers

        if len(requests_responses) > 1:
            result_list = []
            for response in requests_responses:
                body = response.json()
                if isinstance(body, list):
                    result_list += body
                else:
                    result_list.append(body)
            webob_response.body = json.dumps(result_list)
        else:
            webob_response.body = json.dumps(requests_responses[0].json())

        return webob_response

    def _create_forwarded_urls(self, request_url):
        # Extract endpoints from request
        url_pattern = self._find_pattern_for_request(request_url)
        url_pattern_parts = url_pattern.split(ENDPOINTS_WILDCARD)
        match_expression = re.escape(url_pattern_parts[0]) + \
            "(?P<endpoint_ids>.*)" + \
            re.escape(url_pattern_parts[1])
        endpoint_ids = re.match(match_expression, request_url)

        # Extract trailing portion of URL
        trailing_route = request_url[len(url_pattern_parts[0] + endpoint_ids.group("endpoint_ids") + url_pattern_parts[1]):]

        # Create final URLs to be forwarded
        endpoint_urls = []
        for endpoint_id in endpoint_ids.group("endpoint_ids").split(','):
            url = self._endpoints[endpoint_id] + trailing_route
            print url
            endpoint_urls.append(url)

        return endpoint_urls
