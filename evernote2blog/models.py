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


Base.metadata.create_all(engine)
