import json

import requests
import MySQLdb
from bs4 import BeautifulSoup

from config import User_Agent
from config import DB_CONFIG


class Cookies(object):
    def __init__(self):
        self.connection = MySQLdb.connect(
            db=DB_CONFIG['database'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['password'])
        self.cursor = self.connection.cursor()
        self.url = 'http://www.zhihu.com'
        self.headers = {'User-Agent': User_Agent}

    def cookies(self):
        """:return dict"""
        sql = 'select cookies from manage_information limit 1'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()[0].split(';')
        cookies = {}
        for c in result:
            if c.startswith('login'):
                cookies['login'] = c.split('login=')[1]
            if c.startswith('z_c0'):
                cookies['z_c0'] = c.split('z_c0=')[1]
        # r = requests.get(self.url, cookies=cookies, headers=self.headers)
        # soup = BeautifulSoup(r.content, 'lxml')
        # xsrf = soup.find_all('input', attrs={'name': '_xsrf'})
        # if xsrf:
        #     cookies['xsrf'] = xsrf[0].attrs['value']
        return cookies

    def verify_cookie(self):
        cookies = self.cookies()
        r = requests.get(self.url,cookies=cookies, headers=self.headers)
        soup = BeautifulSoup(r.content,'lxml')
        if soup.find_all('a', class_='zu-top-nav-userinfo '):
            return True
        else:
            return False
