import unittest
import json
import sys

import requests

from user_information import UserInformation
from cookies import Cookies
from config import User_Agent


class TestUserInformation(unittest.TestCase):
    c = Cookies()
    url = 'http://www.zhihu.com/people/xia-shou-78/'
    headers = {'User-Agent': User_Agent}
    r = requests.get(url,headers=headers,cookies=c.cookies())
    user_information = UserInformation(r.text)

    def test_a(self):
        pass