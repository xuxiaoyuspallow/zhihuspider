from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AnswerSnapshots(Base):
    __tablename__ = 'answers_snapshots'

    id = Column(primary_key=True)
    answer_id = Column()
    voteup_count = Column()
    comment_count = Column()
    collapsed_counts = Column()
    excerpt = Column()
    can_comment = Column()
    comment_permission = Column()
    is_normal = Column()
    reshipment_settings = Column()
    author = Column()
    question = Column()
    relationship = Column()
    suggest_edit = Column()
    type = Column()
    created_time = Column()
    updated_time = Column()
    crawl_time = Column()


class PostsSnapshots(Base):
    __tablename__ = 'posts_snapshots'

    id = Column(primary_key=True)
    post_id = Column()
    author = Column()
    can_comment = Column()
    collapsed_counts = Column()
    comment_count = Column()
    comment_permission = Column()
    excerpt = Column()
    excerpt_title = Column()
    image_url = Column()
    reviewing_comments_count = Column()
    title = Column()
    type = Column()
    upvoted_followees = []
    voteup_count = Column()
    voting = Column()
    created = Column()
    updated = Column()
    crawl_time = Column()


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(primary_key=True)
    question_id = Column()
    title = Column()
    crawl_time = Column()


class QuestionsSnapshots(Base):
    __tablename__ = 'questions_snapshots'

    id = Column(primary_key=True)
    question_id = Column()
    question_type = Column()
    title = Column()
    type = Column()
    answer_num = Column()
    followers = Column()
    recently = Column()
    views_num = Column()
    topic_follower = Column()
    labels = Column()
    labels_links = Column()
    content = Column()
    crawl_time = Column()


class UserSnapshots(Base):
    __tablename__ = 'user_snapshots'

    id = Column(primary_key=True)
    user_id = Column()
    name = Column()
    avatar = Column()
    answers_num = Column()
    posts_num = Column()
    asks_num = Column()
    followers_num = Column()
    followees_num = Column()
    agrees_num = Column()
    thanks_num = Column()
    be_marked = Column()
    be_collected_num = Column()
    edits_num = Column()
    crawl_time = Column()


class Users(Base):
    __tablename__ = 'users'

    id = Column(primary_key=True)
    user_id = Column()