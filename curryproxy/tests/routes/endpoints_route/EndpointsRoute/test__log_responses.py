# Copyright (c) 2015 Rackspace, Inc.
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
import logging

import mock
from mock import patch
from testtools import TestCase

from curryproxy.routes import EndpointsRoute


class Test__Log_Response(TestCase):

    def setUp(self):
        super(Test__Log_Response, self).setUp()

        self.endpoints_route = EndpointsRoute(
            mock.MagicMock(),
            mock.MagicMock(),
            mock.MagicMock(),
            mock.MagicMock(),
        )

        self.logger = logging.getLogger('curryproxy.routes.endpoints_route')

        patcher = patch.object(logging, 'debug')
        self.logging_debug = patcher.start()
        self.addCleanup(patcher.stop)

    def test_log_level_notset(self):
        self.logger.setLevel(logging.NOTSET)

        self.endpoints_route._log_responses(mock.Mock(), mock.MagicMock())

        self.assertTrue(self.logging_debug.called)

    def test_log_level_debug(self):
        self.logger.setLevel(logging.DEBUG)

        self.endpoints_route._log_responses(mock.Mock(), mock.MagicMock())

        self.assertTrue(self.logging_debug.called)

    def test_log_level_info(self):
        self.logger.setLevel(logging.INFO)

        self.endpoints_route._log_responses(mock.Mock(), mock.MagicMock())

        self.assertFalse(self.logging_debug.called)

    def test_log_level_warning(self):
        self.logger.setLevel(logging.WARNING)

        self.endpoints_route._log_responses(mock.Mock(), mock.MagicMock())

        self.assertFalse(self.logging_debug.called)

    def test_log_level_error(self):
        self.logger.setLevel(logging.ERROR)

        self.endpoints_route._log_responses(mock.Mock(), mock.MagicMock())

        self.assertFalse(self.logging_debug.called)

    def test_log_level_critical(self):
        self.logger.setLevel(logging.CRITICAL)

        self.endpoints_route._log_responses(mock.Mock(), mock.MagicMock())

        self.assertFalse(self.logging_debug.called)
