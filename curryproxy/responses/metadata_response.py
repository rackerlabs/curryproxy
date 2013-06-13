from curryproxy.responses.response_base import ResponseBase


class MetadataResponse(ResponseBase):
    def __init__(self, request, responses):
        super(MetadataResponse, self).__init__(request)
        self._responses = responses
        
        self._aggregate_response_bodies()
