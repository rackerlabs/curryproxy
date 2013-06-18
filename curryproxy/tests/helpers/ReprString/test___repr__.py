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
