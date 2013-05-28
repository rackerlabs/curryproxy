class StartResponseMock(object):
    def __init__(self):
        self._call_count = 0
        self._status = None
        self._headers = None

    def __call__(self, status, headers):
        self._call_count += 1
        self._status = status
        self._headers = headers

    @property
    def call_count(self):
        return self._call_count

    @property
    def status(self):
        return self._status

    @property
    def headers(self):
        return self._headers
