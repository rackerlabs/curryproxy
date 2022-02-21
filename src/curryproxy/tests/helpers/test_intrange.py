from testtools import TestCase

from curryproxy.helpers import intrange


class TestIntrange(TestCase):
    def test_int(self):
        self.assertEqual(intrange(13), [13])

    def test_single_number(self):
        self.assertEqual(intrange("13"), [13])

    def test_range(self):
        self.assertEqual(intrange("17-23"), [17, 18, 19, 20, 21, 22, 23])

    def test_backwards_range(self):
        self.assertRaises(ValueError, intrange, "23-17")

    def test_incomplete_range(self):
        self.assertRaises(ValueError, intrange, "17-")

    def test_overcomplete_range(self):
        self.assertRaises(ValueError, intrange, "17--23")

    def test_wrong_separator(self):
        self.assertRaises(ValueError, intrange, "17:23")

    def test_notarange(self):
        self.assertRaises(ValueError, intrange, "words")
