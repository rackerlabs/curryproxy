from webob import Response

from curryproxy.responses.response_base import ResponseBase


class SingleResponse(ResponseBase):
    def __init__(self, request, response):
        self._request = request
        self._response = Response()

        self._response.status = '{0} {1}'.format(response.status_code,
                                                 response.reason)
        self._response.headers = response.headers
        self._response.body_file = response.raw

        self._fix_headers()

    @property
    def response(self):
        return self._response
