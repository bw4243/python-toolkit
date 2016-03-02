#!/usr/bin/python
# -*-coding:utf-8-*-

from myutils import *
import pyperclip


def login():
    resp = http_retry(
        'http://api.shjmpt.com:9002/pubApi/uLogin?uName=penkie&pWord=penguo1110&Developer=ojF%2f6Xe%2blVBjWugligpxDQ%3d%3d')
    print(resp)

    return resp.split('&')[0]


def get_phones(token, num=10):
    resp = http_retry('http://api.shjmpt.com:9002/pubApi/GetPhone?ItemId=244&token=%s&Count=%d' % (token, num))
    print(resp)
    result = '\n'.join(resp.split(';')[::-1])
    print(result)
    pyperclip.copy(result[1:])
    return resp


def release_phones(token):
    print(http_retry('http://api.shjmpt.com:9002/pubApi/ReleaseAllPhone?token=%s' % token))


def get_msg(token, phone):
    resp = 'False'
    while 'False' in resp:
        resp = http_retry(
            'http://api.shjmpt.com:9002/pubApi/GMessage?token=%s&ItemId=244&Phone=%s' % (token, phone))
        print(resp)
        time.sleep(5)


def get_msg_once(token, phone):
    resp = http_retry(
        'http://api.shjmpt.com:9002/pubApi/GMessage?token=%s&ItemId=244&Phone=%s' % (token, phone))
    print(resp)
    return resp


def exit_login(token):
    print(http_retry('http://api.shjmpt.com:9002/pubApi/uExit?token=%s' % token))


if __name__ == '__main__':
    token = 'VERuxZjwksbyng6APn5ARtK4TAhsX34'  # login()
    # release_phones(token)
    # get_phones(token,5)
    # release_phones(token)
    # exit_login(token)

    get_msg(token, '15992745387')
