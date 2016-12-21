import unittest

from cookies import Cookies


class TestCookie(unittest.TestCase):
    c = Cookies()

    def test_cookies(self):
        self.assertTrue(self.c.verify_cookie())


