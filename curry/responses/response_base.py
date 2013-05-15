class ResponseBase(object):
    def _fix_headers(self):
        # Add gzip encoding if the client supports it
        if (self._response.content_encoding is None
                or self._response.content_encoding
                and 'gzip' not in self._response.content_encoding
                and 'gzip' in self._request.accept_encoding):
            self._response.encode_content()

        # Remove gzip encoding if the client doesn't support it
        if (self._response.content_encoding
                and 'gzip' in self._response.content_encoding
                and 'gzip' not in self._request.accept_encoding):
            self._response.decode_content()
