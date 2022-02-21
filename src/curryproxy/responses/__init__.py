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
"""Responses to be returned to the client.

Modules:
    response_base: Base class for responses.

Classes:
    ErrorResponse: A response to the client if any destination endpoint
        returned an error.
    MetadataResponse: Aggregates metadata about each destination endpoint's
        response.
    MultipleResponse: Represents a response from multiple destinations back to
        the client.
    SingleResponse: Represents a response from a single destination endpoint.
    StatusResponse: A response representing the status of the CurryProxy
        server.

"""
from curryproxy.responses import error_response
from curryproxy.responses import metadata_response
from curryproxy.responses import multiple_response
from curryproxy.responses import single_response
from curryproxy.responses import status_response

# Hoist classes into the package namespace
ErrorResponse = error_response.ErrorResponse
MetadataResponse = metadata_response.MetadataResponse
MultipleResponse = multiple_response.MultipleResponse
SingleResponse = single_response.SingleResponse
StatusResponse = status_response.StatusResponse
