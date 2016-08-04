#!/usr/bin/python
# -*-coding:utf-8-*-

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float
from db import Base, engine, session
from myutils import *


# 定义CommonUser对象:
class BlogConfig(Base):
    # 提供一个共享的查询session,节省性能开销
    __s = session()

    # 表的名字:
    __tablename__ = 'BlogConfig'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    blog_type = Column(String, unique=True)
    evernote_updated_count = Column(Integer)
    evernote_note_count = Column(Integer)
    blog_article_count = Column(Integer)
    add_time = Column(DateTime, default=now())
    update_time = Column(DateTime, default=now(), onupdate=now())
    field1 = Column(String, default='')
    field2 = Column(String, default='')
    field3 = Column(String, default='')


Base.metadata.create_all(engine)
