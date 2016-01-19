#!/usr/bin/python
# -*-coding:utf-8-*-

import sqlite3
import os


def __connect_db():
    current_path = os.path.split(os.path.realpath(__file__))[0]
    return sqlite3.connect(current_path + "/qianka.db")


def new_disciple(idfa, uuid, userid, cookie):
    db = __connect_db()
    db.execute("INSERT INTO disciple(idfa,uuid,userid,cookie) VALUES(?,?,?,?)",
               [idfa, uuid, userid, cookie])
    db.commit()
    db.close()


def fetch_valid(count):
    db = __connect_db()
    cur = db.execute("SELECT idfa,uuid,cookie,userid,contrib FROM disciple WHERE valid=1 LIMIT ?", [count])
    entries = [dict(idfa=row[0], uuid=row[1], cookie=row[2], userid=row[3], contrib=row[4]) for row in cur.fetchall()]
    db.commit()
    db.close()

    return entries


def set_invald(userid):
    db = __connect_db()
    db.execute("UPDATE  disciple SET valid=0 WHERE userid=?", [userid])
    db.commit()
    db.close()


def inc_contrib(userid):
    db = __connect_db()
    db.execute("UPDATE  disciple SET contrib=contrib+1 WHERE userid=?", [userid])
    db.execute("UPDATE  disciple SET valid=0 WHERE userid=? AND contrib>=10", [userid])
    db.commit()
    db.close()


if __name__ == '__main__':
    # new_disciple('sab','sdzzz','123','cookie111')
    print(fetch_valid(1))
    # set_invald('123')
    # inc_contrib('123')
