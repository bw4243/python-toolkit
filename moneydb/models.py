#!/usr/bin/python
# -*-coding:utf-8-*-

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float
from db import Base, engine, session
from myutils import *
from constants import *


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

    def update_is_working(self, is_working):
        self.is_working=is_working
        s = session()
        s.query(User).filter(User.user_id == self.user_id).update({User.is_working: is_working})
        s.commit()
        s.close()

    @staticmethod
    def fetch_valid_users(app_type):
        s = session()
        users = s.query(User).filter(User.valuable == True, User.is_working == False, User.freeze_status == False,
                                     User.app_type == app_type).all()
        s.close()
        return users

    @staticmethod
    def fetch_all(app_type):
        s = session()
        users = s.query(User).filter(User.app_type == app_type).all()
        s.close()
        return users

    @staticmethod
    def fetch_valid_one(user_id):
        s = session()
        user = s.query(User).filter(User.valuable == True, User.is_working == False, User.freeze_status == False,User.user_id == user_id).first()
        s.close()
        return user

    @staticmethod
    def get(user_id):
        s = session()
        user = s.query(User).filter(User.user_id == user_id).one()
        s.close()
        return user

    @staticmethod
    def add(**kwargs):
        # 创建session对象:
        s = session()
        # 添加到session:
        s.add(User(**kwargs))
        # 提交即保存到数据库:
        s.commit()
        # 关闭session:
        s.close()

    # 提供一个共享的查询session,节省性能开销
    __s = session()

    @staticmethod
    def query(*entities, **kwargs):
        if len(entities) == 0:
            return User.__s.query(User, **kwargs)
        else:
            return User.__s.query(*entities, **kwargs)


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

    def update_task_status(self, status):
        self.status = status
        self.update_time = now()
        s = session()
        s.query(Task).filter(Task.id == self.id).update({Task.status: status})
        s.commit()
        s.close()

    def update_task_firetime(self, firetime):
        self.fire_time =firetime
        self.update_time = now()
        s = session()
        s.query(Task).filter(Task.id == self.id).update({Task.fire_time: firetime})
        s.commit()
        s.close()

    # 提供一个共享的查询session,节省性能开销
    __s = session()

    @staticmethod
    def query(*entities, **kwargs):
        if len(entities) == 0:
            return Task.__s.query(Task, **kwargs)
        else:
            return Task.__s.query(*entities, **kwargs)

    @staticmethod
    def fetch_waiting_tasks(app_type):
        s = session()
        tasks = s.query(Task).filter(Task.status == TASK_STATUS_WAIT,
                                     User.app_type == app_type, Task.fire_time < now()).all()

        s.close()
        return tasks


Base.metadata.create_all(engine)
