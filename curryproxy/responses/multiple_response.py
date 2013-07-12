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
    MultipleResponse: Represents a response from multiple destinations back to
        the client.

"""
import json

from curryproxy.responses.response_base import ResponseBase


class MultipleResponse(ResponseBase):
    """Represents a response from multiple destinations back to the client.

    This class will aggregate multiple responses (provided in the constructor)
    from destination endpoints into a single response to be returned to the
    client. Each destination response must be valid JSON. The body of the
    response will be a JSON array consisting of all the items returned from
    destination endpoints.

    """
    def __init__(self, request, responses):
        """Initializes a new MultipleResponse.

        If all destination endpoints responded with a HTTP 200 OK and returned
        JSON, the responses will be added to a JSON array to be returned to the
        client. Otherwise, metadata about each response will be displayed in
        the body of the final response.

        Args:
            request: webob.Request representation of the incoming request.
            responses: List of requests.Response representing responses from
                destination endpoints.

        """
        super(MultipleResponse, self).__init__(request)
        self._responses = responses

        json_returned = all('Content-Type' in response.headers
                            and 'application/json'
                            in response.headers['Content-Type'].lower()
                            for response in responses)
        responses_succeeded = all(response.status_code == 200
                                  for response in responses)

        if (request.method == 'GET'
                and 'application/json' in request.accept
                and json_returned
                and responses_succeeded):
            self._merge_responses()
        else:
            self._aggregate_responses()

        self._fix_headers()

    def _merge_responses(self):
        """Merges multiple JSON responses into a single JSON response array.

        The response status and headers are taken from the first response as
        each response should have similar values here.

        A note about arrays: If a destination endpoint normally returns arrays,
        the array is unpacked before adding its items into the final response
        array. This is to closely mimic the nature of the destination endpoint.
        However, if a destination endpoint normally returns an array of arrays,
        the inner arrays will be preserved in the final response to the client.

        """
        self._response.status = self._responses[0].status_code

        self._response.headers = self._responses[0].headers
        self._response.content_encoding = None

        result_list = []
        for response in self._responses:
            body = response.json()
            if isinstance(body, list):
                result_list += body
            else:
                result_list.append(body)
        self._response.body = json.dumps(result_list)

    def _aggregate_responses(self):
        """Aggregates metadata about multiple responses.

        The highest class-level status code is chosen based on the responses
        received. The response body is aggregated by
        ResponseBase._aggregate_response_bodies() - see that function for more
        information.

        """
        self._response.status = 502
        status_codes = [response.status_code for response in self._responses
                        if response.status_code < 500]

        if len(status_codes) > 1:
            max_status_code = max(status_codes)
            for status_code in [400, 300, 200, 100]:
                if max_status_code / status_code == 1:
                    self._response.status = status_code
                    break

        self._response.content_type = 'application/json'

        self._aggregate_response_bodies()
