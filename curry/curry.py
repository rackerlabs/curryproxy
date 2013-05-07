import json

from route import Route
from errors import RouteError


class Curry(object):
    def __init__(self, routes_file='/etc/curry/routes.json'):
        self._routes = []
        self._process_routes(routes_file)

    def _process_routes(self, routes_file):
        try:
            route_config = json.load(open(routes_file))
        except ValueError:
            raise RouteError('Configuration file contains invalid JSON.')

        for route_dict in route_config:
            self._routes.append(Route(route_dict))
