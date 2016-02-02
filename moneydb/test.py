#!/usr/bin/python
# -*-coding:utf-8-*-
import datetime

import db
from models import *
from myutils import *
from constants import *

# db.add(QiankaUser(idfa='abc2', uuid='fuck2', userid='1232',master_id='12',cookie='cookie2'))

s = db.session()

# db.add(User(user_id='123', nick_name=u'盆锅222', app_type='xiaobing', oid_md5='ABCDF'
#                   , idfa='idfa', idfv='idfv', uid='123333', cookie='cookie1',
#                   valuable=True, is_working=True, balance=1.0, today_income=10.0, total_income=20.0,
#                   add_time=now(), update_time=now()))

# print(s.query(CommonUser).get(2))

# print(s.query(CommonUser).filter(CommonUser.add_time < now()).all())
# print(s.query(CommonUser).filter(CommonUser.add_time < now()).all())

# s.query(CommonUser).filter(CommonUser.id == 2).update({CommonUser.balance: 200})
# s.commit()
#
# s.close()
#
# s.query(CommonUser).filter(CommonUser.id == 2).delete()
# s.commit()
# s.close()

# print(s.query(QiankaUser).all())
#
# print(s.query(QiankaUser.prentice_count).filter_by(userid='1232').all())

# print(s.query(QiankaUser).filter(QiankaUser.userid=='123'))


# for k in QiankaUser.__dict__.keys():
#     print(k,QiankaUser.__dict__[k])



# s.add(Task(common_user_id=2, task_id='456', task_name='taskname222', bundle_id='com.sdfs.sfsd',
#                  process_name='sdf', status=TASK_STATUS_WAIT, block_type=BLOCKED_TYPE_ONE, fire_time=now(),
#                  app_type=APP_TYPE_XIAO_BIN, add_time=now(), update_time=now()))
#
# s.commit()
#
# print(s.query(Task).filter(Task.task_id=='456').all())


# s.query(Task).filter(Task.common_user_id == 1).update({Task.status: TASK_STATUS_COMPLETED})
s.commit()
s.close()


