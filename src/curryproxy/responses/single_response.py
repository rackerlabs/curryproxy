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
    SingleResponse: Represents a response from a single destination endpoint.

"""
from curryproxy.responses.response_base import ResponseBase


class SingleResponse(ResponseBase):
    """Represents a response from a single destination endpoint."""
    def __init__(self, request, response):
        """Initializes a new SingleResponse

        When CurryProxy only communicates with a single destination endpoint,
        the data it receives back should be returned to the client with as
        little modification as possible. This class represents this case.

        Args:
            request: webob.Request representation of the incoming request.
            response: requests.Response representation of the response from the
                destination endpoint.

        """
        super(SingleResponse, self).__init__(request)

        self._response.status = '{0} {1}'.format(response.status_code,
                                                 response.reason)
        self._response.headers = response.headers
        self._response.body_file = response.raw

        self._fix_headers()
