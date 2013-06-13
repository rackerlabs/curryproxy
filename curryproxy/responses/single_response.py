from curryproxy.responses.response_base import ResponseBase


class SingleResponse(ResponseBase):
    def __init__(self, request, response):
        super(SingleResponse, self).__init__(request)

        self._response.status = '{0} {1}'.format(response.status_code,
                                                 response.reason)
        self._response.headers = response.headers
        self._response.body_file = response.raw

        self._fix_headers()
