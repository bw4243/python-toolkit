#!/usr/bin/python
# -*-coding:utf-8-*-

from myutils import *
import xiangta


def query():
    url = 'http://t1.ronganjx.com/Web11/logging/BookingCWStudy.aspx?coachName=9114046400&date=2016-02-20&beginTime=0800&trainType=%E5%9C%BA%E5%A4%96&timeLine=9'
    resp = http_retry(url, headers={'Cookie': 'ASP.NET_SessionId=ftn2tpiwitdzg3nrrazxff55'})
    # print(resp)
    if '无当天场次信息' in resp:
        print('no')
    else:
        print('yes')
        xiangta.send_notify('')


if __name__ == '__main__':
    while 1:
        query()
        time.sleep(2)
