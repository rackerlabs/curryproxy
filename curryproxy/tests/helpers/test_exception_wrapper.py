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
