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
        sql = 'select * from cookies limit 1'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()[4].split(';')
        cookies = {}
        cookies[result[0].split('=')[0]] = result[0].split('=')[1]
        cookies[result[1].split('=')[0]] = result[0].split('=')[1]
        r = requests.get(self.url, cookies=cookies, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        xsrf = soup.find_all('input',attrs={'name':'_xsrf'})[0].attrs['value']
        if xsrf:
            cookies['xsrf'] = xsrf
        return cookies

    def verify_cookie(self):
        cookies = self.cookies()
        r = requests.get(self.url,cookies=cookies, headers=self.headers)
        soup = BeautifulSoup(r.text,'lxml')
        if soup.find_all('a', class_='zu-top-nav-userinfo '):
            return True
        else:
            return False

if __name__ == '__main__':
    c = Cookies()
    headers = {'User-Agent': User_Agent}
    cookies = c.cookies()
    headers['authorization'] = 'Bearer ' + cookies['z_c0']
    r = requests.get(
        url='https://www.zhihu.com/api/v4/members/zhang-jia-wei/answers?sort_by=created&per_page=5&include=data%5B%2A%5D.is_normal%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.voting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=5&offset=5',
        headers=headers,
        cookies=cookies
    )
    with open('g.html','w') as f :
        f.write((r.text).encode('utf-8'))
    from pprint import pprint
    result = json.loads(r.text)
    pprint(json.loads(r.text))