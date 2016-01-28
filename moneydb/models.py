#!/usr/bin/python
# -*-coding:utf-8-*-

from sqlalchemy import Column, String, Integer
from db import Base


# 定义QiankaUser对象:
class QiankaUser(Base):
    # 表的名字:
    __tablename__ = 'QiankaUser'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    idfa = Column(String)
    uuid = Column(String)
    cookie = Column(String)
    userid = Column(String)
    master_id = Column(String)
    contrib = Column(Integer, default=0)
    valuable = Column(Integer, default=1)
    has_uncompleted = Column(Integer, default=0)
    start_time = Column(Integer, default=0)
    wait_seconds = Column(Integer, default=0)
    now_task = Column(String)
    freeze_status = Column(Integer, default=0)
    balance = Column(String, default='0')
    today_income = Column(String, default='0')
    total_income = Column(String, default='0')
    withdraw_realname = Column(String)
    prentice_count = Column(Integer, default=0)

    def __repr__(self):
        return '{id:%d,userid:%s}' % (self.id,self.userid)

# 定义ShikeUser对象:
class ShikeUser(Base):
    # 表的名字:
    __tablename__ = 'ShikeUser'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    idfa = Column(String)
    uuid = Column(String)
    cookie = Column(String)
    userid = Column(String)
    master_id = Column(String)
    contrib = Column(Integer, default=0)
    valuable = Column(Integer, default=1)
    has_uncompleted = Column(Integer, default=0)
    start_time = Column(Integer, default=0)
    wait_seconds = Column(Integer, default=0)
    now_task = Column(String)
    freeze_status = Column(Integer, default=0)
    balance = Column(String, default='0')
    today_income = Column(String, default='0')
    total_income = Column(String, default='0')
    withdraw_realname = Column(String)
    prentice_count = Column(Integer, default=0)

    def __repr__(self):
        return '{id:%d,userid:%s}' % (self.id,self.userid)