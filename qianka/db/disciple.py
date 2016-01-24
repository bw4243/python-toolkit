#!/usr/bin/python
# -*-coding:utf-8-*-

import sqlite3
import os
import time


def __connect_db():
    # current_path = os.path.split(os.path.realpath(__file__))[0]
    current_path = '/data/dbs'
    return sqlite3.connect(current_path + "/qianka.db")


def new_disciple(idfa, uuid, userid, cookie, master_id):
    db = __connect_db()
    db.execute("INSERT INTO disciple(idfa,uuid,userid,cookie,master_id) VALUES(?,?,?,?,?)",
               [idfa, uuid, userid, cookie, master_id])
    db.commit()
    db.close()


def fetch_valid(count):
    db = __connect_db()
    cur = db.execute(
        "SELECT id,idfa,uuid,cookie,userid,master_id,contrib,valuable,has_uncompleted,start_time,wait_seconds,now_task FROM disciple WHERE valuable=1 AND has_uncompleted=0 LIMIT ? ",
        [count])
    entries = [dict(id=row[0], idfa=row[1], uuid=row[2], cookie=row[3], userid=row[4], master_id=row[5], contrib=row[6],
                    valuable=row[7],
                    has_uncompleted=row[8], start_time=row[9], wait_seconds=row[10],
                    now_task=row[11].decode('unicode-escape')) for row in
               cur.fetchall()]
    db.commit()
    db.close()

    return entries


def fetch_all():
    db = __connect_db()
    cur = db.execute(
        "SELECT id,idfa,uuid,cookie,userid,master_id,contrib,valuable,has_uncompleted,start_time,wait_seconds,now_task,freeze_status FROM disciple "
    )
    entries = [dict(id=row[0], idfa=row[1], uuid=row[2], cookie=row[3], userid=row[4], master_id=row[5], contrib=row[6],
                    valuable=row[7],
                    has_uncompleted=row[8], start_time=row[9], wait_seconds=row[10],
                    now_task=row[11].decode('unicode-escape'), freeze_status=row[12]) for row in
               cur.fetchall()]
    db.commit()
    db.close()

    return entries


def fetch_masters():
    db = __connect_db()
    cur = db.execute(
        "SELECT id,idfa,uuid,cookie,userid,master_id,contrib,valuable,has_uncompleted,start_time,wait_seconds,now_task,freeze_status,balance,today_income,total_income,withdraw_realname,prentice_count FROM disciple WHERE master_id=0"
    )
    entries = [dict(id=row[0], idfa=row[1], uuid=row[2], cookie=row[3], userid=row[4], master_id=row[5], contrib=row[6],
                    valuable=row[7],
                    has_uncompleted=row[8], start_time=row[9], wait_seconds=row[10],
                    now_task=row[11].decode('unicode-escape'), freeze_status=row[12],
                    balance=row[13], today_income=row[14], total_income=row[15],
                    withdraw_realname=row[16].encode('utf-8'), prentice_count=row[17]) for row in
               cur.fetchall()]
    db.commit()
    db.close()

    return entries


def fetch_will_complete():
    db = __connect_db()
    cur = db.execute(
        "SELECT id,idfa,uuid,cookie,userid,master_id,contrib,valuable,has_uncompleted,start_time,wait_seconds,now_task FROM disciple WHERE has_uncompleted=1 AND start_time + wait_seconds < ? ",
        [int(time.time())])
    entries = [dict(id=row[0], idfa=row[1], uuid=row[2], cookie=row[3], userid=row[4], master_id=row[5], contrib=row[6],
                    valuable=row[7],
                    has_uncompleted=row[8], start_time=row[9], wait_seconds=row[10],
                    now_task=row[11].decode('unicode-escape')) for row in
               cur.fetchall()]
    db.commit()
    db.close()

    return entries


def set_invaluable(userid):
    db = __connect_db()
    db.execute("UPDATE  disciple SET valuable=0 WHERE userid=?", [userid])
    db.commit()
    db.close()


def update_task_info(bean):
    db = __connect_db()
    db.execute("UPDATE  disciple SET has_uncompleted=?,start_time=?,wait_seconds=?,now_task=? WHERE id=?",
               [bean['has_uncompleted'], bean['start_time'], bean['wait_seconds'], bean['now_task'], bean['id']])
    db.commit()
    db.close()


def inc_contrib(userid):
    db = __connect_db()
    db.execute("UPDATE  disciple SET contrib=contrib+1 WHERE userid=?", [userid])
    db.execute("UPDATE  disciple SET valuable=0 WHERE userid=? AND contrib>=3 AND master_id!=0", [userid])
    db.commit()
    db.close()


def update_account_status(id, freeze_status, balance, total_income, today_income, prentice_count):
    db = __connect_db()
    db.execute(
        "UPDATE  disciple SET freeze_status=?,balance=?,total_income=?,today_income=?,prentice_count=? WHERE id=?",
        [freeze_status, balance, total_income, today_income, prentice_count, id])
    db.commit()
    db.close()


if __name__ == '__main__':
    # new_disciple('sab2', 'sdzzz2', '1232', 'cookie11122', '12')
    # print(fetch_valid(2))
    # set_invald('123')
    # inc_contrib('123')
    # import json
    #
    # json.loads('')
    #
    # data = fetch_valid(1)
    # print(data)
    #
    # print((data[0]['now_task']))


    # print(fetch_will_complete())


    print(fetch_masters())
    # print(fetch_masters()[0]['withdraw_realname'])

    # data[0]['has_uncompleted'] = 1
    # data[0]['start_time'] = int(time.time())
    # data[0]['wait_seconds']=30
    # data[0]['now_task'] = json.dumps({'id':'123','title':'我是周知哦那个'})
    # update_task_info(data[0])
