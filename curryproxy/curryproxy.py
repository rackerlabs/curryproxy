import json
import logging

from webob import Request
from webob import Response

from errors import ConfigError
from errors import RequestError
from routes import route_factory


def exception_wrapper(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logging.exception(e)

    return wrapper


class CurryProxy(object):
    def __init__(self,
                 routes_file='/etc/curryproxy/routes.json',
                 logging_config='/etc/curryproxy/logging.conf'):
        self._routes = []
        self._process_routes(routes_file)
        logging.config.fileConfig(logging_config)

    def _process_routes(self, routes_file):
        try:
            route_configs = json.load(open(routes_file))
        except ValueError:
            raise ConfigError('Configuration file contains invalid JSON.')

        for route_config in route_configs:
            self._routes.append(route_factory.parse_dict(route_config))

    @exception_wrapper
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = None

        try:
            matched_route = self._match_route(request.url)
            response = matched_route.issue_request(request)
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
