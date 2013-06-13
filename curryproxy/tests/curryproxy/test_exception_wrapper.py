from mock import patch
from testtools import TestCase

from curryproxy.curryproxy import exception_wrapper


class TestException_Wrapper(TestCase):
    def test_wrapper(self):
        custom_exception = Exception('Custom Exception')

        @exception_wrapper
        def test_method():
            raise custom_exception

        with patch('logging.exception') as le:
            test_method()

            le.assert_called_with(custom_exception)
