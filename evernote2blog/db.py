#!/usr/bin/python
# -*-coding:utf-8-*-


from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine('sqlite:////data/dbs/blogconfig.db', encoding='UTF-8', echo=True)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


def session():
    return DBSession()
