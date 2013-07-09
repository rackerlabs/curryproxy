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
from testtools import TestCase

from curryproxy.helpers import ReprString


class Test__Repr__(TestCase):
    def test___repr__(self):
        test_str = 'I am a\nstring with some\twhitespace characters'
        test_repr = repr(test_str)
        # Sanity check
        self.assertNotEqual(test_str, test_repr)

        repr_string = ReprString(test_str)

        self.assertEqual(test_str, repr(repr_string))
        self.assertNotEqual(test_repr, repr(repr_string))
