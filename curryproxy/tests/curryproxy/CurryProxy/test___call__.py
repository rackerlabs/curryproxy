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
from mock import patch
from testtools import TestCase
from webob import Response

from curryproxy import CurryProxy
from curryproxy.routes import ForwardingRoute
from curryproxy.routes import route_factory
from curryproxy.tests.utils import StartResponseMock


class Test__Call__(TestCase):
    def setUp(self):
        super(Test__Call__, self).setUp()

        self.curry = CurryProxy('curryproxy/tests/etc/routes.empty.json',
                                'curryproxy/tests/etc/logging.console.conf')

    def test_matched_route(self):
        # Setup route
        self.route_config = {'route': 'https://www.example.com',
                             'forwarding_url': 'https://new.example.com'}
        self.route = route_factory.parse_dict(self.route_config)
        self.curry._routes.append(self.route)

        # Mocked response
        mock_response = Response()
        mock_response.status = 200
        mock_response.body = 'Response Body'

        # Create request
        environ = {'wsgi.url_scheme': 'https',
                   'HTTP_HOST': 'www.example.com',
                   'PATH_INFO': '/path',
                   'QUERY_STRING': 'query=string'}
        start_response = StartResponseMock()

        # Issue request
        with patch.object(ForwardingRoute,
                          '__call__',
                          return_value=mock_response):
            response = self.curry.__call__(environ, start_response)

            # Assert
            self.assertEqual(mock_response.status, start_response.status)
            self.assertEqual(mock_response.headerlist, start_response.headers)
            self.assertEqual(mock_response.body, response)

    def test_unmatched_route(self):
        environ = {'wsgi.url_scheme': 'https',
                   'HTTP_HOST': 'www.example.com',
                   'PATH_INFO': '/path',
                   'QUERY_STRING': 'query=string'}
        start_response = StartResponseMock()

        response = self.curry.__call__(environ, start_response)

        self.assertEqual('403 Forbidden', start_response.status)
        self.assertIsNotNone(response)
