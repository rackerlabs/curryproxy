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
    StatusResponse: A response representing the status of the CurryProxy
        server.

"""
import json
import platform

from curryproxy.responses.response_base import ResponseBase


class StatusResponse(ResponseBase):
    """A response representing the status of the CurryProxy server."""
    def __init__(self, request):
        """Initializes a new StatusResponse.

        Since CurryProxy is simply a WSGI application we can safely say that it
        is "up" by returning the host machine's name.

        Args:
            request: webob.Request representation of the incoming request.

        """
        super(StatusResponse, self).__init__(request)

        self._response.headers['Content-Type'] = 'application/json'
        self._response.body = json.dumps({'hostname': platform.node()})

        self._fix_headers()
