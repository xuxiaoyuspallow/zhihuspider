# coding:utf-8
"""
data-flow:
1.take all users from table Users
2.crawl users_snapshots
3.crawl answers_snapshots、posts_snapshots and followees
4.and answers_snapshots、posts_snapshots to related tables
5.and suitable followees to table users
6.suitable followees: 1000 agrees, 100 followers and at least one answer
"""
import time
import threading
import Queue

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cookies import Cookies
from user_information import UserInformation
from user_detail import UserDetail
from config import DB_CONFIG, User_Agent
from models import Users, UserSnapshots
from models import AnswerSnapshots, PostsSnapshots
from models import Questions


engine = create_engine(
    'mysql://{user}:{password}@{host}/{database}'.format(
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        database=DB_CONFIG['database']
    ),convert_unicode=True)
session = sessionmaker(bind=engine)()


class Main(object):
    def __init__(self,user_id, cookies):
        super(Main, self).__init__()
        self.id = user_id
        self.cookies = cookies
        self.user_detail = UserDetail(user_id,cookies)
        self.headers = {
            'User-Agent': User_Agent
        }

    def user_snapshots(self):
        user_snapshot_url = 'http://www.zhihu.com/people/{id}'.format(id=self.id)
        r = requests.get(user_snapshot_url, headers=self.headers,cookies=self.cookies)
        user_info = UserInformation(r.text)
        us = UserSnapshots(
            id=0,
            user_id=self.id,
            name=user_info.name(),
            avatar=user_info.avatar(),
            answers_num=user_info.answer(),
            posts_num=user_info.post(),
            asks_num=user_info.ask(),
            followers_num=user_info.follower(),
            followees_num=user_info.followee(),
            agrees_num=user_info.agree(),
            thanks_num=user_info.thanks(),
            be_marked=user_info.marked(),
            be_collected_num=user_info.be_collected(),
            edits_num=user_info.logs(),
            crawl_time=int(time.time())
        )
        session.add(us)
        session.commit()

    def answers_snapshot(self,data):
        an_s = AnswerSnapshots(
            id=0,
            answer_id=data['id'],
            voteup_count=data['voteup_count'],
            comment_count=data['comment_count'],
            collapsed_counts=data['collapsed_counts'],
            excerpt=data['excerpt'].encode('utf-8'),
            can_comment=unicode(data['can_comment']).encode('utf-8'),
            comment_permission=data['comment_permission'],
            is_normal=data['is_normal'],
            reshipment_settings=data['reshipment_settings'],
            author=unicode(data['author']).encode('utf-8'),
            question=unicode(data['question']).encode('utf-8'),
            relationship=unicode(data['relationship']).encode('utf-8'),
            suggest_edit=unicode(data['suggest_edit']).encode('utf-8'),
            type=data['type'],
            created_time=data['created_time'],
            updated_time=data['updated_time'],
            crawl_time=int(time.time())
        )
        session.add(an_s)
        session.commit()

    def questions(self,data):
        if_exit = session.query(Questions.question_id).filter(Questions.question_id==self.id).scalar()
        if if_exit:
            pass

    def question_snapshots(self,data):
        pass

    def posts_snapshots(self,data):
        pass

    def user(self,data):
        pass

    def start(self):
        self.user_snapshots()
        self.user_detail.answers(20)
        # self.user_detail.posts(20)
        # self.user_detail.followees(20)
        while not self.user_detail.answers_queue.empty():
            data = self.user_detail.answers_queue.get()
            self.answers_snapshot(data)
            self.question_snapshots(data['question'])
            self.questions(data['question'])
        while not self.user_detail.post_queue.empty():
            data = self.user_detail.post_queue.get()
            self.posts_snapshots(data)
        while not self.user_detail.followings_queue.empty():
            data = self.user_detail.followings_queue.get()
            self.user(data)


if __name__ == '__main__':
    c = Cookies()
    if c.verify_cookie():
        cookies = c.cookies()
    else:
        import sys
        sys.exit()
    tasks = session.query(Users).all()
    task_queue = Queue.Queue()
    for task in tasks:
        task_queue.put(task.user_id.strip())
    for i in range(1):
        while not task_queue.empty():
            m = Main(task_queue.get(),cookies)
            t = threading.Thread(target=m.start)
            t.start()
            t.join()
            del t
