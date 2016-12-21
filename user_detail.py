# coding=utf-8
import json
import Queue
import logging

import requests

from cookies import Cookies
from config import User_Agent

logging.basicConfig(level='INFO')


class UserDetail(object):
    def __init__(self, _id, cookies):
        self.id = _id
        self.base_url = 'https://www.zhihu.com/people/{id}/'.format(id=self.id)
        self.cookies = cookies
        self.headers = {
            'User-Agent': User_Agent
        }
        self.answers_queue = Queue.Queue()
        self.post_queue = Queue.Queue()
        self.followings_queue = Queue.Queue()

    def answers(self, limit):
        answer_api = 'https://www.zhihu.com/api/v4/members/{id}/answers'.format(id=self.id)
        params = {
            'sort_by': 'created',
            'limit': 1,
            'offset': 0,
        }
        r = requests.get(answer_api,params=params, headers=self.headers, cookies=self.cookies)
        result = json.loads(r.text)
        if not result['data']:
            logging.info(u'{id}没有回答')
            return True
        total = result['paging']['totals']
        for i in range(0,total,limit):
            logging.info(u'正在爬行{0}的答案: {1}%'.format(self.id,0 if not i else int(float(i)*100//total)))
            params = {
                'sort_by': 'created',
                'per_page': 5,
                'include': 'data[*].is_normal,suggest_edit,comment_count,collapsed_counts,'
                           'reviewing_comments_count,can_comment,voteup_count,reshipment_settings,'
                           'comment_permission,mark_infos,created_time,updated_time,'
                           'relationship.voting,is_author,is_thanked,is_nothelp,upvoted_followees;'
                           'data[*].author.badge[?(type=best_answerer)].topics',
                'limit': limit,
                'offset': i,
            }
            r = requests.get(answer_api, params=params, headers=self.headers, cookies=self.cookies)
            result = json.loads(r.text)
            for data in result['data']:
                self.answers_queue.put(data)
        logging.info(u'{id}的回答已爬行完成，总条数为{total}'.format(id=self.id,total=total))
        return True

    def posts(self,limit):
        post_api = 'https://www.zhihu.com/api/v4/members/{id}/articles'.format(id=self.id)
        params = {
            'sort_by': 'created',
            'limit': 1,
            'offset': 0,
        }
        r = requests.get(post_api, params=params, headers=self.headers, cookies=self.cookies)
        result = json.loads(r.text)
        if not result['data']:
            logging.info(u'{id}没有文章')
            return True
        total = result['paging']['totals']
        for i in range(0, total, limit):
            logging.info(u'正在爬行{0}的文章: {1}%'.format(self.id,0 if not i else int(float(i) * 100 // total)))
            params = {
                'sort_by': 'created',
                'include': 'data[*].comment_count,collapsed_counts,reviewing_comments_count,'
                           'can_comment,comment_permission,voteup_count,created,updated,'
                           'upvoted_followees,voting;data[*].author.badge[?(type=best_answerer)].topics',
                'limit': limit,
                'offset': i,
            }
            r = requests.get(post_api, params=params, headers=self.headers, cookies=self.cookies)
            result = json.loads(r.text)
            for data in result['data']:
                self.post_queue.put(data)
        logging.info(u'{id}的文章已爬行完成，总条数为{total}'.format(id=self.id, total=total))
        return True

    def followees(self,limit):
        followees_api = 'https://www.zhihu.com/api/v4/members/{id}/followees'.format(id=self.id)
        params = {
            'limit': 1,
            'offset': 0,
        }
        r = requests.get(followees_api, params=params, headers=self.headers, cookies=self.cookies)
        result = json.loads(r.text)
        if not result['data']:
            logging.info(u'{id}没有关注的人')
            return True
        total = result['paging']['totals']
        for i in range(0, total, limit):
            logging.info(u'正在爬行{0}关注的人: {1}%'.format(self.id,0 if not i else int(float(i) * 100 // total)))
            params = {
                'include': 'data[*].column.title,intro,description,followers,articles_count',
                'limit': limit,
                'offset': i,
            }
            r = requests.get(followees_api, params=params, headers=self.headers, cookies=self.cookies)
            result = json.loads(r.text)
            for data in result['data']:
                self.followings_queue.put(data)
        logging.info(u'{id}的关注的人已爬行完成，总条数为{total}'.format(id=self.id, total=total))
        return True

    def followers(self):
        pass

if __name__ == '__main__':
    c = Cookies()
    u = UserDetail('zhang-jia-wei',c.cookies())
    u.followees(20)