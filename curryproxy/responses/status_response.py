import json
import platform

from curryproxy.responses.response_base import ResponseBase


class StatusResponse(ResponseBase):
    def __init__(self, request):
        super(StatusResponse, self).__init__(request)

        self._response.headers['Content-Type'] = 'application/json'
        self._response.body = json.dumps({'hostname': platform.node()})

        self._fix_headers()
