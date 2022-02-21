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
    ErrorResponse: A response to the client if any destination endpoint
      returned an error.

"""
from curryproxy.responses.response_base import ResponseBase
from curryproxy.responses.single_response import SingleResponse


class ErrorResponse(ResponseBase):
    """A response to the client if any destination endpoint returned an error.

    If any errors were encountered from destination endpoints, this class will
    determine which error(s) should be returned back to the client.

    """
    def __init__(self, request, responses, priority_errors):
        """Initializes a new ErrorResponse.

        If any priority errors have been defined for the route generating this
        error they should be passed in here. If any response code matched a
        priority error status code, only that response will be returned. If
        multiple destination responses matched a priority error status code,
        one will be chosen at random to be returned to the client.

        If no priority error status codes were received but there was still a
        client-level (400-class) status code, only the client-level error
        response will be returned. If multiple destination responses returned
        client-level error status codes, one will be chosen at random to be
        returned to the client.

        Finally, if neither of the two previous clauses apply, a HTTP 502 Bad
        Gateway is returned and metadata about each response is aggregated into
        the body as described in ResponseBase._aggregate_response_bodies().

        Args:
            request: webob.Request representation of the incoming request.
            response: List of requests.Response representing responses from
                destination endpoints.
            priority_errors: List of error status codes to be immediately
                returned if encountered.

        """
        super(ErrorResponse, self).__init__(request)
        self._responses = responses

        status_codes = [r.status_code for r in responses]
        priority_error = next((pe for pe in priority_errors
                               if pe in status_codes),
                              None)

        error_status_code = priority_error
        if error_status_code is None:
            error_status_code = next((sc for sc in status_codes
                                      if sc >= 400 and sc < 500),
                                     None)

        error_response = next(
            (
                r for r in responses
                if r.status_code == error_status_code and
                error_status_code is not None
            ),
            None,
        )
        if error_response is not None:
            single_response = SingleResponse(request, error_response)
            self._response = single_response.response
        else:
            self._response.status = 502
            self._aggregate_response_bodies()
