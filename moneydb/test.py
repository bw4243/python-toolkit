#!/usr/bin/python
# -*-coding:utf-8-*-

import db
from models import QiankaUser

# db.add(QiankaUser(idfa='abc2', uuid='fuck2', userid='1232',master_id='12',cookie='cookie2'))


s = db.session()


# print(s.query(QiankaUser).all())
#
# print(s.query(QiankaUser.prentice_count).filter_by(userid='1232').all())

# print(s.query(QiankaUser).filter(QiankaUser.userid=='123'))


# for k in QiankaUser.__dict__.keys():
#     print(k,QiankaUser.__dict__[k])


def tt(*c):
    print(c)


tt(QiankaUser.userid == '11')

print(type(QiankaUser.userid))
