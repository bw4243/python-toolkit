#!/usr/bin/python
# -*-coding:utf-8-*-


from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

print('db.py invoked')

# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine('sqlite:////data/dbs/money.db', encoding='UTF-8', echo=False)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


def add(entity):
    # 创建session对象:
    s = DBSession()
    # 添加到session:
    s.add(entity)
    # 提交即保存到数据库:
    s.commit()
    # 关闭session:
    s.close()



def session():
    return DBSession()
