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
