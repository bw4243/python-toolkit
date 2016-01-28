#!/usr/bin/python
# -*-coding:utf-8-*-


from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

print('db.py invoked')

# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine('sqlite:////data/dbs/money.db')
engine.echo = True
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


def add(new_user):
    # 创建session对象:
    session = DBSession()
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()

def session():
    return DBSession()
