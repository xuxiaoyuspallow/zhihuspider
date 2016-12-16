# coding: utf-8
import requests
from bs4 import BeautifulSoup


class UserInformation(object):
    def __init__(self,html):
        self.soup = BeautifulSoup(html,'lxml')

    def avatar(self):
        return self.soup.find_all('img',class_='Avatar Avatar--large UserAvatar-inner')[0].attrs['src']

    def signature(self):
        return self.soup.find_all('span', class_='RichText ProfileHeader-headline')[0].text

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

    def answer(self):
        result = self.soup.find_all('li',attrs={'aria-controls':'Profile-answers'})[0].contents[0].text[2:]
        return int(result)

    def post(self):
        result = self.soup.find_all('li', attrs={'aria-controls': 'Profile-posts'})[0].contents[0].text[2:]
        return int(result)

    def ask(self):
        result = self.soup.find_all('li', attrs={'aria-controls': 'Profile-asks'})[0].contents[0].text[2:]
        return int(result)

    def following(self):
        result = self.soup.find_all('div', class_='Profile-followStatusValue')[0].text
        return int(result)

    def follower(self):
        result = self.soup.find_all('div', class_='Profile-followStatusValue')[1].text
        return int(result)


class Links(object):
    def __init__(self, _id):
        self.id = _id
        self.base_url = 'https://www.zhihu.com/people/{id}/'.format(id=self.id)

    def followers(self):
        pass

    def followings(self):
        pass

    def anwsers(self):
        pass

    def posts(self):
        pass
