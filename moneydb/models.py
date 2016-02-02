#!/usr/bin/python
# -*-coding:utf-8-*-

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float
from db import Base, engine
from myutils import *


# 定义CommonUser对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'User'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True)
    nick_name = Column(String)
    app_type = Column(String)
    cookie = Column(String)
    idfa = Column(String)
    oid_md5 = Column(String, default='')
    idfv = Column(String, default='')
    uid = Column(String, default='')
    valuable = Column(Boolean, default=True)
    is_working = Column(Boolean, default=False)
    freeze_status = Column(Boolean, default=False)
    balance = Column(Float, default=0)
    today_income = Column(Float, default=0)
    total_income = Column(Float, default=0)
    add_time = Column(DateTime, default=now())
    update_time = Column(DateTime, default=now(), onupdate=now())
    field1 = Column(String, default='')
    field2 = Column(String, default='')
    field3 = Column(String, default='')

    def __repr__(self):
        return '{id=%d,user_id=%s}' % (self.id, self.user_id)


class Task(Base):
    # 表的名字:
    __tablename__ = 'Task'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    task_id = Column(String)
    task_name = Column(String, default='')
    bundle_id = Column(String)
    process_name = Column(String)
    status = Column(String)
    block_type = Column(String)
    fire_time = Column(DateTime)
    app_type = Column(String)
    add_time = Column(DateTime, default=now())
    update_time = Column(DateTime, default=now(), onupdate=now())
    field1 = Column(String, default='')
    field2 = Column(String, default='')
    field3 = Column(String, default='')

    def __repr__(self):
        return '{id=%d,user_id=%s}' % (self.id, self.user_id)


Base.metadata.create_all(engine)
