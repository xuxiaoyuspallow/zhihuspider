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
import logging
import json

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cookies import Cookies
from user_information import UserInformation
from user_detail import UserDetail
from config import DB_CONFIG, User_Agent
from config import New_User
from models import Users, UserSnapshots
from models import AnswerSnapshots, PostsSnapshots
from models import Questions, QuestionsSnapshots
from question import Question


engine = create_engine(
    'mysql://{user}:{password}@{host}/{database}'.format(
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        database=DB_CONFIG['database']
    ),convert_unicode=True)
session = sessionmaker(bind=engine)()


class Main(threading.Thread):
    def __init__(self, cookies):
        super(Main, self).__init__()
        self.cookies = cookies
        self.headers = {
            'User-Agent': User_Agent
        }

    def user_snapshots(self,user_id):
        user_snapshot_url = 'http://www.zhihu.com/people/{id}'.format(id=user_id)
        r = requests.get(user_snapshot_url, headers=self.headers,cookies=self.cookies)
        user_info = UserInformation(r.content)
        us = UserSnapshots(
            id=0,
            user_id=user_id,
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
        logging.info("adding usersnapshot")
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
        logging.info("adding answersnapshot")
        session.add(an_s)
        session.commit()

    def questions(self,data):
        if_exit = session.query(Questions.question_id).filter(Questions.question_id==data['id']).scalar()
        if not if_exit:
            q = Questions(
                id=0,
                question_id=data['id'],
                title=data['title'],
                crawl_time=int(time.time())
            )
            logging.info("adding question")
            session.add(q)
            session.commit()

    def question_snapshots(self,data):
        url = 'http://www.zhihu.com/question/{id}'.format(id=data['id'])
        try:
            r = requests.get(url, cookies=self.cookies, headers=self.headers)
        except Exception as e:
            logging.error(e)
            return
        else:
            q = Question(r.content)
            followers = q.follower()
            views_num = q.viewer()
            answer_num = q.answer()
            if not answer_num or not views_num or not followers:
                return
            q_s = QuestionsSnapshots(
                id=0,
                question_id=data['id'],
                question_type=data['type'],
                title=data['title'],
                type=data['type'],
                answer_num=answer_num,
                followers=followers,
                recently=q.recently(),
                views_num=views_num,
                topic_follower=q.topic_followers(),
                labels=q.label(),
                labels_links=q.labels_links(),
                content=q.content(),
                crawl_time=int(time.time())
            )
            logging.info("adding questionsnapshot")
            session.add(q_s)
            session.commit()

    def posts_snapshots(self,data):
        p_s = PostsSnapshots(
            id=0,
            post_id=data['id'],
            author=json.dumps(data['author']),
            can_comment=json.dumps('can_comment'),
            collapsed_counts=data['collapsed_counts'],
            comment_count=data['comment_count'],
            comment_permission=data['comment_permission'],
            excerpt=data['excerpt'],
            excerpt_title=data['excerpt_title'],
            image_url=data['image_url'],
            reviewing_comments_count=data['reviewing_comments_count'],
            title=data['title'],
            type=data['type'],
            upvoted_followees=json.dumps(data['upvoted_followees']),
            voteup_count=data['voteup_count'],
            voting=data['voting'],
            created=data['created'],
            updated=data['updated'],
            crawl_time=int(time.time())
        )
        logging.info("adding postsnapshot")
        session.add(p_s)
        session.commit()

    def user(self,data):
        """"""
        if_exit = session.query(Users.user_id).filter(Users.user_id == data['url_token']).scalar()
        if not if_exit:
            try:
                url = 'http://www.zhihu.com/people/{id}'.format(id=data['url_token'])
                r = requests.get(url,cookies=self.cookies,headers=self.headers)
            except Exception as e:
                logging.error(e)
                return
            else:
                u_i = UserInformation(r.content)
                if u_i.follower() >= New_User['followers'] and u_i.agree() >= New_User['agree'] and u_i.answer() >= New_User['answer']:
                    u = Users(
                        id=0,
                        user_id=data['url_token']
                    )
                    logging.info("adding user")
                    session.add(u)
                    session.commit()

    def run(self):
        while not task_queue.empty():
            task = task_queue.get()
            self.user_snapshots(task)
            user_detail = UserDetail(task,self.cookies)
            user_detail.answers(20)
            user_detail.posts(20)
            user_detail.followees(20)
            while not user_detail.answers_queue.empty():
                data = user_detail.answers_queue.get()
                self.answers_snapshot(data)
                logging.info("adding answersnapshot")
                self.questions(data['question'])
                # self.question_snapshots(data['question'])
            while not user_detail.post_queue.empty():
                data = user_detail.post_queue.get()
                self.posts_snapshots(data)
            while not user_detail.followings_queue.empty():
                data = user_detail.followings_queue.get()
                self.user(data)


if __name__ == '__main__':
    while True:
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
        THREAD = []
        for i in range(10):
            t = Main(cookies)
            t.start()
            THREAD.append(t)
        for t in THREAD:
            t.join()