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
    CurryProxy: WSGI callable responsible for handling requests and returning
        responses.

"""
import json
import logging
import logging.config

from webob import Request
from webob import Response

from curryproxy.errors import ConfigError
from curryproxy.errors import RequestError
from curryproxy.helpers import ENVIRON_REQUEST_UUID_KEY
from curryproxy.helpers import exception_wrapper
from curryproxy.helpers import profile_wrapper
from curryproxy.routes import route_factory


class CurryProxy(object):
    """WSGI callable responsible for handling requests and returning responses.

    A fast and performant proxy and aggregator for querying multiple instances
    of an API spread across globally distributed data centers.

    """
    def __init__(self,
                 routes_file='/etc/curryproxy/routes.json',
                 logging_config='/etc/curryproxy/logging.conf'):
        """Initialize a new CurryProxy server.

        Create an instance of CurryProxy to use with a WSGI-compatible web
        server. The instance of CurryProxy adheres to PEP 333 as a WSGI
        application.

        Args:
            routes_file: Path to CurryProxy's main configuration file which
                details the routes to be served and the backend endpoints each
                route points to. If unspecified, defaults to
                /etc/curryproxy/routes.json.
            logging_config: Path to CurryProxy's logging configuration file. If
                unspecified, defaults to /etc/curryproxy/logging.conf.

        """
        self._routes = []
        self._process_routes(routes_file)
        logging.config.fileConfig(logging_config)

    def _process_routes(self, routes_file):
        """Read a configuration file and setup an instance of CurryProxy.

        Args:
            routes_file: Path to CurryProxy's main configuration file which
                details the routes to be served and the backend endpoints each
                route points to.

        """
        try:
            route_configs = json.load(open(routes_file))
        except ValueError:
            raise ConfigError('Configuration file contains invalid JSON.')

        for route_config in route_configs:
            self._routes.append(route_factory.parse_dict(route_config))

    @exception_wrapper
    @profile_wrapper
    def __call__(self, environ, start_response):
        """Callable method for WSGI applications.

        Each request to CurryProxy starts here. First, match the incoming
        request to a configured route. Then pass the request to the matching
        route. Finally, return the response received from the matching route
        back to the client.

        If a route cannot be found to handle the request, return a 403
        Forbidden.

        Args:
            environ: Dictionary representing the incoming request as specified
                by PEP 333.
            start_response: Callable used to begin the HTTP response as
                specified by PEP 333.

        """
        request = Request(environ)
        response = None

        logging.info('Received request: %s',
                     request.url,
                     extra={'request_uuid': environ[ENVIRON_REQUEST_UUID_KEY]})

        try:
            matched_route = self._match_route(request.url)
            response = matched_route(request)
        except RequestError as request_error:
            response = Response()
            response.status = 403
            response.body = json.dumps(str(request_error))

        start_response(response.status, response.headerlist)
        return response.body

    def _match_route(self, request_url):
        """Matches an incoming request to a configured route.

        Args:
            request_url: URL of the incoming request.

        Returns:
            Route matching the incoming request.

        Raises:
            RequestError: A suitable route wasn't found to handle the incoming
                request.

        """
        for route in self._routes:
            if route.match(request_url):
                return route

        raise RequestError('Unable to find a route to handle the request '
                           'to {0}'.format(request_url))
