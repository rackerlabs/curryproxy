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
import uuid

from mock import patch
from testtools import TestCase

from curryproxy.helpers import exception_wrapper


class TestException_Wrapper(TestCase):
    def test_exception(self):
        custom_exception = Exception('Custom Exception')

        @exception_wrapper
        def test_method(self, environ, start_response):
            raise custom_exception

        with patch('logging.exception') as le:
            test_method(None, {}, None)

            args, kwargs = le.call_args
            self.assertEqual(args[0], custom_exception)

    def test_request_uuid(self):
        @exception_wrapper
        def test_method(self, environ, start_response):
            return environ

        environ = test_method(None, {}, None)

        self.assertTrue('curryproxy.request_uuid' in environ)

        # Reconstruct the uuid to verify validity
        uuid.UUID(environ['curryproxy.request_uuid'])
