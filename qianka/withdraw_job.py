#!/usr/bin/python
# -*-coding:utf-8-*-


import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from db import disciple
import userinfo
import time

if __name__ == '__main__':
    while 1:
        for data in disciple.fetch_masters():
            amount = 100
            if float(data['balance']) >= amount:
                userinfo.weixin_withdraw(data['cookie'], data['withdraw_realname'], amount)
        time.sleep(3)
