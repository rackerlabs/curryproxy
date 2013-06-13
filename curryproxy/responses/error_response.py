from curryproxy.responses.response_base import ResponseBase
from curryproxy.responses.single_response import SingleResponse


class ErrorResponse(ResponseBase):
    def __init__(self, request, responses, priority_errors):
        super(ErrorResponse, self).__init__(request)
        self._responses = responses

        status_codes = [r.status_code for r in responses]
        priority_error = next((pe for pe in priority_errors
                               if pe in status_codes),
                              None)

        error_status_code = priority_error
        if not error_status_code:
            error_status_code = next((sc for sc in status_codes
                                      if sc >= 400 and sc < 500),
                                     None)

        if error_status_code:
            error_response = next(r for r in responses
                                  if r.status_code == error_status_code)
            single_response = SingleResponse(request, error_response)
            self._response = single_response.response
        else:
            self._response.status = 502
            self._aggregate_response_bodies()
