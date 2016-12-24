# coding=utf-8
import re
import json
import logging

import requests
from bs4 import BeautifulSoup

from config import User_Agent
from cookies import Cookies


class Question(object):
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html,'lxml')

    def answer(self):
        try:
            result = re.search(r'\d+',self.soup.select('#zh-question-answer-num')[0].text).group(0)
            return int(result)
        except Exception as e:
            logging.error(e)

    def follower(self):
        try:
            result = re.search(r'\d+',self.soup.find_all('div',class_='zg-gray-normal')[0].text).group(0)
            return int(result)
        except Exception as e:
            logging.error(e)
            return

    def viewer(self):
        try:
            result = re.findall(r'\d+', self.soup.find_all('div', class_='zg-gray-normal')[2].text)
            return int(result[0])
        except Exception as e:
            logging.error(e)

    def topic_followers(self):
        try:
            result = re.findall(r'\d+',self.soup.find_all('div',class_='zg-gray-normal')[2].text)
            return int(result[1])
        except Exception as e:
            logging.error(e)

    def recently(self):
        try:
            result = self.soup.find_all('span',class_='time')[0].text
            return result
        except Exception as e:
            logging.error(e)

    def label(self):
        # todo: unicode 编码
        tags = self.soup.find_all('a', class_='zm-item-tag')
        result = []
        for tag in tags:
            result.append(tag.text.strip())
        return json.dumps(result)

    def labels_links(self):
        # todo: unicode 编码
        links = self.soup.find_all('a', class_='zm-item-tag')
        result = []
        for link in links:
            temp = {link.text.strip(): link.attrs['href']}
            result.append(temp)
        return json.dumps(result)

    def content(self):
        try:
            c = self.soup.select('#zh-question-detail')[0].text
            return c.strip() if not u'写补充说明' == c.strip() else None
        except Exception as e:
            logging.error(e)




if __name__ == '__main__':
    headers = {
        'User-Agent': User_Agent
    }
    c = Cookies()
    cookies = c.cookies()
    url = 'http://www.zhihu.com/question/20552556'
    r = requests.get(url,headers=headers,cookies=cookies)
    q = Question(r.content)
    print q.follower()

