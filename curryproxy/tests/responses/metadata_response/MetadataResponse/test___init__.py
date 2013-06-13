from mock import patch
from testtools import TestCase

from curryproxy.responses import MetadataResponse
from curryproxy.tests.utils import RequestsResponseMock


class Test__Init__(TestCase):
    def test__aggregate_response_bodies(self):
        with patch.object(MetadataResponse, '_aggregate_response_bodies') as m:
            headers = {'Content-Type': 'text/html'}
            response_1 = RequestsResponseMock(status_code=200, headers=headers)
            response_2 = RequestsResponseMock(status_code=502, headers=headers)

            MetadataResponse(None, [response_1, response_2])

            m.assert_called_with()
