from mock import Mock
from mock import patch
from testtools import TestCase

from curryproxy import helpers
from curryproxy.helpers import profile_wrapper


# http://docs.python.org/2/howto/logging.html#logging-levels
LOGGING_LEVEL_INFO = 20


class TestProfileWrapper(TestCase):
    def test_logging_level_profile_off(self):
        self._patch_logging(LOGGING_LEVEL_INFO)

        with patch('logging.debug') as ld:
            self._wrapped_method(None, None)
            self.assertFalse(ld.called)

    def test_logging_level_profile_on(self):
        self._patch_logging(helpers.LOGGING_LEVEL_DEBUG)

        with patch('logging.debug') as ld:
            self._wrapped_method({'curryproxy.request_uuid': 'N/A'}, None)
            self.assertTrue(ld.called)

    def _patch_logging(self, effective_level):
        getEffectiveLevel = Mock(return_value=effective_level)
        getLogger = Mock(getEffectiveLevel=getEffectiveLevel)
        self.patcher = patch('logging.getLogger', return_value=getLogger)
        self.patcher.start()

    @profile_wrapper
    def _wrapped_method(self, environ, start_response):
        pass

    def tearDown(self):
        super(TestProfileWrapper, self).tearDown()
        self.patcher.stop()
