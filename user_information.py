# coding: utf-8
import json

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

    def agree(self):
        pass

    def thanks(self):
        pass

    def be_collected(self):
        pass

    def logs(self):
        pass


class UserDetail(object):
    def __init__(self, _id):
        self.id = _id
        self.base_url = 'https://www.zhihu.com/people/{id}/'.format(id=self.id)

    def followers(self):
        pass

    def followings(self):
        pass

    def answers(self):
        url = self.base_url + 'answer'
        params = {
            'sort_by': 'created',
            'per_page': 5,
            'include': 'data[*].is_normal,suggest_edit,comment_count,collapsed_counts,'
                       'reviewing_comments_count,can_comment,voteup_count,reshipment_settings,'
                       'comment_permission,mark_infos,created_time,updated_time,'
                       'relationship.voting,is_author,is_thanked,is_nothelp,upvoted_followees;'
                       'data[*].author.badge[?(type=best_answerer)].topics',
            'limit': 5,
            'offset': 5,
        }
        answer_api = 'https://www.zhihu.com/api/v4/members/{id}/answers'.format(id=self.id)
        r = requests.get(answer_api,params=params)
        result = json.loads(r.text)
        assert isinstance(json.loads(r.text),dict)



    def posts(self):
        pass
