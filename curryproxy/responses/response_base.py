from datetime import datetime
import json

from webob import Response


class ResponseBase(object):
    def __init__(self, request):
        self._request = request
        self._response = Response()

    def _aggregate_response_bodies(self):
        results = []
        for response in self._responses:
            if response is None:
                results.append(None)
                continue

            result = {}
            result['url'] = response.url
            result['status'] = '{0} {1}'.format(response.status_code,
                                                response.reason)
            result['headers'] = dict(response.headers)
            result['body'] = response.content

            results.append(result)

        self._response.body = json.dumps(results)

    def _fix_headers(self):
        self._fix_content_encoding()
        self._fix_date()

    def _fix_content_encoding(self):
        # Add gzip encoding if the client supports it
        if (self._response.content_encoding is None
                or 'gzip' not in self._response.content_encoding
                and self._request.accept_encoding
                and 'gzip' in self._request.accept_encoding):
            self._response.encode_content(encoding='gzip')

        # Remove gzip encoding if the client doesn't support it
        if (self._request.accept_encoding is None
                or self._response.content_encoding
                and 'gzip' in self._response.content_encoding
                and 'gzip' not in self._request.accept_encoding):
            self._response.decode_content()

    def _fix_date(self):
        self._response.date = datetime.utcnow()

    @property
    def response(self):
        return self._response
