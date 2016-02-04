#!/usr/bin/python
# -*-coding:utf-8-*-

from myutils import  *

def send_notify(text):
    content='arg=send_clock&ct=2&ih=1&remind_date=2016-02-04%2014%3A36%3A09&target_phonenumber=18521058664&text_clock=%E8%AE%B0%E5%BE%97%E5%93%A6&token=5b9f1927b1b78dc1cac85a34241306ae&uid=38571'
    resp=http_retry('http://115.28.175.70/api/3000.php',method='POST',headers={'Cookie':'PHPSESSID=utv7dabprj817ij085lgbeit50','Content-Type': 'application/x-www-form-urlencoded'},body=content)
    print(resp)


if __name__ == '__main__':
    send_notify('')