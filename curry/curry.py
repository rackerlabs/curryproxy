import json
from urlparse import urlparse

from webob import Response, Request
import requests

from route import Route
from errors import ConfigError, RequestError


class Curry(object):
    def __init__(self, routes_file='/etc/curry/routes.json'):
        self._routes = []
        self._process_routes(routes_file)

    def _process_routes(self, routes_file):
        try:
            route_config = json.load(open(routes_file))
        except ValueError:
            raise ConfigError('Configuration file contains invalid JSON.')

        for route_dict in route_config:
            self._routes.append(Route(route_dict))

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = None

        try:
            matched_route = self._match_route(request.url)
            response = self._issue_request(request, matched_route)
        except RequestError as re:
            response = Response()
            response.status = 403
            response.body = str(re)

        start_response(response.status, response.headerlist)
        return response.body

    def _match_route(self, request_url):
        for route in self._routes:
            if route.match(request_url):
                return route

        raise RequestError('Unable to find a route to handle the request '
                           'to {0}'.format(request_url))

    def _issue_request(self, incoming_request, route):
        destination_url = route.create_forwarded_url(incoming_request.url)
        incoming_request.headers['Host'] = urlparse(destination_url).netloc

        requests_response = requests.request(incoming_request.method,
                                             destination_url,
                                             data=incoming_request.body,
                                             headers=incoming_request.headers,
                                             allow_redirects=False,
                                             verify=True)

        webob_response = Response()
        webob_response.status = requests_response.status_code
        webob_response.headers = requests_response.headers
        webob_response.body = requests_response.content

        return webob_response
