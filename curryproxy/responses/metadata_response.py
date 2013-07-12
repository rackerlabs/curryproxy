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
    MetadataResponse: Aggregates metadata about each destination endpoint's
        response.

"""
from curryproxy.responses.response_base import ResponseBase


class MetadataResponse(ResponseBase):
    """Aggregates metadata about each destination endpoint's response."""
    def __init__(self, request, responses):
        """Initializes a new instance of MetadataResponse.

        This response will always return a HTTP 200 OK. The response body will
        contain metadata about each destination endpoint's response as outlined
        in ResponseBase._aggregate_response_bodies().

        Args:
            request: webob.Request representation of the incoming request.
            responses: List of requests.Response representing responses from
                destination endpoints.

        """
        super(MetadataResponse, self).__init__(request)
        self._responses = responses

        self._aggregate_response_bodies()
