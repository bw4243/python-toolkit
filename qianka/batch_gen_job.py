#!/usr/bin/python
# -*-coding:utf-8-*-


import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import httplib
import time
import userinfo
from db import disciple

if __name__ == '__main__':
    while 1:
        userinfo.batch_gen('33005806', count=40)

        time.sleep(3)
