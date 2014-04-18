# Copyright (c) 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from mock import Mock
from requests import Response


class RequestsResponseMock(Response):
    def __init__(self,
                 url=None,
                 status_code=None,
                 reason=None,
                 headers=None,
                 body=None):
        super(RequestsResponseMock, self).__init__()

        # hasattr call is protection against upstream changes in requests
        if hasattr(self, 'url'):
            self.url = url
        else:
            raise AttributeError()

        if hasattr(self, 'status_code'):
            self.status_code = status_code
        else:
            raise AttributeError()

        if hasattr(self, 'reason'):
            self.reason = reason
        else:
            raise AttributeError()

        if hasattr(self, 'headers'):
            self.headers = headers
        else:
            raise AttributeError()

        if hasattr(self, 'raw'):
            stream = Mock()
            stream.read = Mock(side_effect=[body, None])
            stream.stream = Mock(side_effect=AttributeError())
            self.raw = stream
        else:
            raise AttributeError()


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
