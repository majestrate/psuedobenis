from oniichan import templates
from oniichan import util
from oniichan import config
from sqlalchemy import create_engine, asc, desc
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import operator
import os

_engine = create_engine(config.db_url)

make_session = sessionmaker(bind=_engine)

_Base = declarative_base()

@contextmanager
def open():
    sess = make_session()
    yield session(sess)
    sess.close()

class session:

    def __init__(self, sess):
        self.sess = sess
        self.query = sess.query
        self.execute = sess.execute
        self.add = sess.add

    def commit(self):
        self.sess.commit()


    def check_local_login(self, username, password):
        """
        verify a mod login
        """
        user = self.sess.query(LocalUser).filter(LocalUser.username == username).first()
        return user is not None and user.password == util.hash_func(password, user.salt)


    def add_local_user(self, username, password):
        """
        create new mod with credentials
        return None if already exists
        """
        if self.sess.query(LocalUser).filter(LocalUser.username == username).count() > 0:
            return
        user = LocalUser()
        user.username = username
        user.salt = util.new_salt()
        user.password = util.hash_func(password, user.salt)
        self.sess.add(user)
        return user

class LocalUser(_Base):
    __tablename__ = 'localusers'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    salt = Column(String)


class LocalPost(_Base):
    __tablename__ = 'posts'
    internal_id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    text = Column(Text)
    subject = Column(String)
    name = Column(String)

    def __lt__(self, post):
        return self.date < post.date

    def __gt__(self, post):
        return self.date > post.date

    def __le__(self, post):
        return self.date <= post.date

    def __ge__(self, post):
        return self.date >= post.date

    def has_file(self):
        return self.fname is not None and self.fpath is not None

    def is_i2p(self):
        return self.desthash is not None

    def render(self):
        return templates.render_post(self)

    def get_file_url(self):
        if self.fpath is None:
            return ''
        else:
            return '/media/%s' % self.fpath.split('/')[-1]

    def getDate(self):
        return str(self.date).split('.')[0]

    def get_thread_path(self, sess):
        board = sess.query(Board).filter(Board.id == self.board_id).first()
        id = self.post_id if self.reply_id == 0 else self.reply_id
        return os.path.join(board.get_dir(),'thread-%s.html' % id)

    def get_url(self, sess):
        board = sess.query(Board).filter(Board.id == self.board_id).first()
        id = self.post_id if self.reply_id == 0 else self.reply_id
        return '/%s/thread-%s.html' % ( board.name, id)



_Base.metadata.create_all(_engine)
