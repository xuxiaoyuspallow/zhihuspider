import json

import requests
from bs4 import BeautifulSoup

from cookies import Cookies
from config import User_Agent

def test1():
    headers = {
        'User-Agent': User_Agent
    }
    url = 'htps://www.zhihu.com/people/------/answers'
    c =  Cookies()
    cookies = c.cookies()
    r = requests.get(url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(r.text,'lxml')
    result = soup.find_all('div', class_='Profile-sideColumnItem')
    print result

def main():
    try:
        test1()
    except Exception as e:
        print e
        print 1+1

main()