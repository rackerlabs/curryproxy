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
"""Contains a base class for responses.

Classes:
    ResponseBase: Base class for responses.

"""
from datetime import datetime
import json

from webob import Response


class ResponseBase(object):
    """Base class for responses.

    Attributes:
        response: A webob.Response to be returned to the client.

    """
    def __init__(self, request):
        """Initializes a basic response.

        Each response keeps an internal record of its initiating request with
        this base constructor. An empty webob.Response to be returned to the
        client is also created here (in most cases, the response will be
        modified after its creation here before being returned to the client).

        Args:
            request: webob.Request representation of the incoming request.

        """
        self._request = request
        self._response = Response()

    def _aggregate_response_bodies(self):
        """Aggregates multiple responses into one summarizing JSON response.

        Creates a "meta-response" containing information about all responses
        received from destination endpoints. If a connection to a destination
        endpoint fails, a None entry will appear. Otherwise, each entry will
        contain the destination URL, HTTP status & reason, headers, and body.

        Returns:
            A "meta-response" containing information about all responses
            received from destination endpoints.

        """
        results = []
        for response in self._responses:
            if response is None:
                results.append(None)
                continue

            result = {}
            result['url'] = response.url
            result['status'] = '{0} {1}'.format(response.status_code,
                                                response.reason)
            result['headers'] = dict(response.headers)
            result['body'] = response.content

            results.append(result)

        self._response.body = json.dumps(results)
        self._response.content_type = 'application/json'

    def _fix_headers(self):
        """Adjusts the Content-Encoding and Date headers if needed."""
        self._fix_content_encoding()
        self._fix_date()

    def _fix_content_encoding(self):
        """Adjusts the Content-Encoding header if needed.

        Ensures the Content-Encoding of the response will be accepted by the
        original requestor. CurryProxy automatically attempts to use gzip
        encoding when communicating with destination endpoints even if the
        original client doesn't support gzip. Likewise, a response from a
        destination endpoint may not be gzip-encoded even if a requestor were
        to support the encoding. As such, we must either encode or decode the
        response to the original requestor depending on what it supports and on
        what the destination endpoints returned.

        """
        # Add gzip encoding if the client supports it
        if (self._response.content_encoding is None
                or 'gzip' not in self._response.content_encoding
                and self._request.accept_encoding
                and 'gzip' in self._request.accept_encoding):
            self._response.encode_content(encoding='gzip')

        # Remove gzip encoding if the client doesn't support it
        if (self._request.accept_encoding is None
                or self._response.content_encoding
                and 'gzip' in self._response.content_encoding
                and 'gzip' not in self._request.accept_encoding):
            self._response.decode_content()

    def _fix_date(self):
        """Adjusts the Date header.

        Since CurryProxy is modifying responses in some cases, modify the Date
        header to reflect the time the response was created.

        """
        self._response.date = datetime.utcnow()

    @property
    def response(self):
        """A webob.Response to be returned to the client."""
        return self._response
