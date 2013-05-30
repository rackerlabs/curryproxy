import json

from webob import Response

from curryproxy.responses.response_base import ResponseBase


class MultipleResponse(ResponseBase):
    def __init__(self, request, responses):
        self._request = request
        self._responses = responses
        self._response = Response()

        json_returned = all(response.headers['Content-Type'] is not None
                            and 'application/json'
                            in response.headers['Content-Type'].lower()
                            for response in responses)
        responses_succeeded = all(response.status_code == 200
                                  for response in responses)

        if (request.method == 'GET'
                and 'application/json' in request.accept
                and json_returned
                and responses_succeeded):
            self._merge_responses()
        else:
            self._aggregate_responses()

        self._fix_headers()

    def _merge_responses(self):
        self._response.status = self._responses[0].status_code

        self._response.headers = self._responses[0].headers
        self._response.content_encoding = None

        result_list = []
        for response in self._responses:
            body = response.json()
            if isinstance(body, list):
                result_list += body
            else:
                result_list.append(body)
        self._response.body = json.dumps(result_list)

    def _aggregate_responses(self):
        status_codes = [response.status_code for response in self._responses]
        max_status_code = max(status_codes)
        for status_code in [500, 400, 300, 200, 100]:
            if max_status_code / status_code == 1:
                self._response.status = status_code
                break

        self._response.content_type = 'application/json'

        results = []
        for response in self._responses:
            result = {}
            result['url'] = response.url
            result['status'] = '{0} {1}'.format(response.status_code,
                                                response.reason)
            result['headers'] = dict(response.headers)
            result['body'] = response.content

            results.append(result)

        self._response.body = json.dumps(results)

    @property
    def response(self):
        return self._response
