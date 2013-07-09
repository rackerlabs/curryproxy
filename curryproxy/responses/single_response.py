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
