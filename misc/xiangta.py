#!/usr/bin/python
# -*-coding:utf-8-*-

from myutils import *


def send_notify(remind_date,phone,text):
    content = 'arg=send_clock&ct=2&ih=1&remind_date=%s&target_phonenumber=%s&text_clock=%s&token=5e2fe41505f76c16ece3ba27fcfd3475&uid=38571'%(urllib.quote(remind_date) ,phone,urllib.quote(text.encode('utf-8')))
    resp = http_retry('http://115.28.175.70/api/3000.php', method='POST',
                      headers={'Cookie': 'PHPSESSID=4iua27c92gg3lf7buiq263him7',
                               'User-Agent': 'RingIt/3.0 (iPhone; iOS 8.3; Scale/2.00)',
                               'Content-Type': 'application/x-www-form-urlencoded'}, body=content)
    print(resp.decode('unicode-escape'))
    return resp.decode('unicode-escape')


if __name__ == '__main__':
    send_notify(nowtime_str(),'18217681078',u'测试哈2')
