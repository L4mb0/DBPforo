from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from database import connector

class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    username = Column(String(12))

class Post(connector.Manager.Base):
    __tablename__ = 'posts'
    id = Column(Integer, Sequence('message_id_seq'), primary_key=True)
    title = Column(String(100))
    content = Column(String(500))
    posted_on = Column(DateTime, default=datetime.datetime.utcnow)
    user_from_id = Column(Integer, ForeignKey('users.id'))
    user_from = Column(String(100))

class Comment(connector.Manager.Base):
    __tablename__ = 'comments'
    id = Column(Integer, Sequence('comment_id_seq'), primary_key=True)
    content = Column(String(500))
    posted_on = Column(DateTime(timezone=True))
    user_from = Column(String(100))
    post_id = Column(Integer, ForeignKey('posts.id'))