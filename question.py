# coding=utf-8
import re
import requests
from bs4 import BeautifulSoup

from config import User_Agent
from cookies import Cookies


class Question(object):
    def __init__(self, html):
        self.soup = BeautifulSoup(html,'lxml')

    def answer(self):
        result = re.search(r'\d+',self.soup.select('#zh-question-answer-num')[0].text)
        return int(result)

    def follower(self):
        result = re.search(r'\d+',self.soup.find_all('div',class_='zg-gray-normal')[0].text).group(0)
        return int(result)

    def viewer(self):
        result = re.findall(r'\d+', self.soup.find_all('div', class_='zg-gray-normal')[2].text)
        return int(result[0])

    def topic_followers(self):
        result = re.findall(r'\d+',self.soup.find_all('div',class_='zg-gray-normal')[2].text)
        return int(result[1])

    def recently(self):
        result = self.soup.find_all('span',class_='time')[0].text
        return result

    def label(self):
        tags = self.soup.find_all('a', class_='zm-item-tag')
        result = []
        for tag in tags:
            result.append(tag.text.strip())
        return result

    def labels_links(self):
        links = self.soup.find_all('a', class_='zm-item-tag')
        result = []
        for link in links:
            temp = {link.text.strip(): link.attrs['href']}
            result.append(temp)
        return result

    def content(self):
        c = self.soup.select('#zh-question-detail')[0].text
        return c.strip() if not u'写补充说明' == c.strip() else None




if __name__ == '__main__':
    headers = {
        'User-Agent': User_Agent
    }
    c = Cookies()
    cookies = c.cookies()
    url = 'http://www.zhihu.com/question/19614805'
    r = requests.get(url,headers=headers,cookies=cookies)
    q = Question(r.text)
    print q.content()

