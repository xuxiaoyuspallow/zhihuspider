# coding: utf-8
import re

from bs4 import BeautifulSoup


class UserInformation(object):
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')

    def name(self):
        result = self.soup.find_all('span',class_='ProfileHeader-name')[0].text
        print result
        return result

    def avatar(self):
        result = self.soup.find_all('img',class_='Avatar Avatar--large UserAvatar-inner')[0].attrs['src']
        return result

    def signature(self):
        result = self.soup.find_all('span', class_='RichText ProfileHeader-headline')[0].text
        return result

    def answer(self):
        result = self.soup.find_all('li',attrs={'aria-controls':'Profile-answers'})[0].contents[0].text[2:]
        return int(result)

    def post(self):
        result = self.soup.find_all('li', attrs={'aria-controls': 'Profile-posts'})[0].contents[0].text[2:]
        return int(result)

    def ask(self):
        result = self.soup.find_all('li', attrs={'aria-controls': 'Profile-asks'})[0].contents[0].text[2:]
        return int(result)

    def followee(self):
        result1 = self.soup.find_all('div', class_='Profile-followStatusValue')
        if result1:
            result = result1[0].text
        result2 = self.soup.find_all('div', class_='NumberBoard-value')
        if result2:
            result = result2[0].text
        return int(result)

    def follower(self):
        result1 = self.soup.find_all('div', class_='Profile-followStatusValue')
        if result1:
            result = result1[1].text
        result2 = self.soup.find_all('div', class_='NumberBoard-value')
        if result2:
            result = result2[1].text
        return int(result)

    def agree(self):
        result = self.soup.find_all('div', class_='Profile-sideColumnItem')
        for ele in result:
            if u'赞同' in ele.text:
                num = re.findall(r'\d+', ele.text)
                if num:
                    return int(num[0])

    def thanks(self):
        result = self.soup.find_all('div', class_='Profile-sideColumnItem')
        for ele in result:
            if u'感谢' in ele.text:
                num = re.findall(r'\d+', ele.text)
                if num:
                    return int(num[1])

    def be_collected(self):
        result = self.soup.find_all('div', class_='Profile-sideColumnItem')
        for ele in result:
            if u'收藏' in ele.text:
                num = re.findall(r'\d+', ele.text)
                if num:
                    return int(num[2])

    def logs(self):
        result = self.soup.find_all('div', class_='Profile-sideColumnItem')
        for ele in result:
            if u'公共编辑' in ele.text:
                num = re.findall(r'\d+', ele.text)
                if num:
                    return int(num[0])

    def marked(self):
        result = self.soup.find_all('div', class_='Profile-sideColumnItem')
        for ele in result:
            if u'知乎收录' in ele.text:
                num = re.search(r'\d+',ele.text)
                if num:
                    return int(num.group(0))

    def description(self):
        pass

    def location(self):
        pass

    def business(self):
        pass

    def employment(self):
        pass

    def education(self):
        pass

    def educationextra(self):
        pass

if __name__ == '__main__':
    import requests
    from cookies import Cookies
    from config import User_Agent
    c = Cookies()
    url = 'https://www.zhihu.com/people/------/answers'
    headers = {'User-Agent': User_Agent}
    r = requests.get(url, headers=headers, cookies=c.cookies())
    u = UserInformation(r.text)
    print u.name()
    print u.agree()
    print u.answer()
    print u.avatar()
    print u.signature()
    print u.answer()
    print u.post()
    print u.ask()
    print u.follower()
    print u.followee()
    print u.logs()
    print u.marked()
