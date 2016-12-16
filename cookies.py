import requests
import MySQLdb
from bs4 import BeautifulSoup

from config import HEADER
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

    def cookies(self):
        """:return dict"""
        sql = 'select * from cookies limit 1'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()[4].split(';')
        cookies = {}
        cookies[result[0].split('=')[0]] = result[0].split('=')[1]
        cookies[result[1].split('=')[0]] = result[0].split('=')[1]
        r = requests.get(self.url, cookies=cookies, headers=HEADER)
        soup = BeautifulSoup(r.text, 'lxml')
        xsrf = soup.find_all('input',attrs={'name':'_xsrf'})[0].attrs['value']
        if xsrf:
            cookies['xsrf'] = xsrf
        return cookies

    def verify_cookie(self):
        cookies = self.cookies()
        r = requests.get(self.url,cookies=cookies, headers=HEADER)
        soup = BeautifulSoup(r.text,'lxml')
        if soup.find_all('a', class_='zu-top-nav-userinfo '):
            return True
        else:
            return False

if __name__ == '__main__':
    c = Cookies()
    print c.verify_cookie()