from datetime import datetime

from webob import Response


class ResponseBase(object):
    def __init__(self, request):
        self._request = request
        self._response = Response()

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
