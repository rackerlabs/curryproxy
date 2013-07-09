"""The classes in this module have been lifted into the package namespace.

Classes:
    MetadataResponse: Aggregates metadata about each destination endpoint's
        response.

"""
from curryproxy.responses.response_base import ResponseBase


class MetadataResponse(ResponseBase):
    """Aggregates metadata about each destination endpoint's response."""
    def __init__(self, request, responses):
        """Initializes a new instance of MetadataResponse.

        This response will always return a HTTP 200 OK. The response body will
        contain metadata about each destination endpoint's response as outlined
        in ResponseBase._aggregate_response_bodies().

        Args:
            request: webob.Request representation of the incoming request.
            responses: List of requests.Response representing responses from
                destination endpoints.

        """
        super(MetadataResponse, self).__init__(request)
        self._responses = responses

        self._aggregate_response_bodies()
