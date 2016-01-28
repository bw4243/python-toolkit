#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib
import json
import threading
import urllib
import os
import time
import datetime
from pyDes import *
import base64
from moneydb.models import ShikeUser
from myutils import *


def get_header(cookie):
    return {
        'Cookie': cookie,
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": 'zh-cn',
        "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
        "Connection": 'keep-alive',
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
    }


def encryptContent(str, replace=1):
    Des_Key = "0dxwLxO8"  # Key
    Des_IV = "\x01\x02\x03\x04\x05\x06\x07\x08"  # IV向量
    k = des(Des_Key, CBC, Des_IV, padmode=PAD_PKCS5)
    encryptstr = k.encrypt(str)
    ret = base64.b64encode(encryptstr)  # 转base64编码返回
    if replace:
        ret = ret.replace('+', '%2B')
    else:
        ret = urllib.quote_plus(ret)
    # ret = ret.replace('+', '%2B')

    print(ret)
    return ret


lastTryIncome = 0
succeed = False


def getUserFinance(shike_user):
    url = 'http://itry.com/itry/income/getUserFinance'
    content = 'openidMD5=%s&cur_time=%d' % (shike_user.oid_md5, datetime.datetime.now().microsecond)

    str = http_retry(url, method='POST', body=content, headers=get_header(shike_user.cookie))

    obj = json.loads(str)
    # print(response.read())
    # print('今日收入:%s' % obj['today_income'].encode('UTF-8'))
    global lastTryIncome, succeed
    nowTryIncome = float(obj['try_income'].encode('UTF-8')[:-3])
    if lastTryIncome == 0:
        lastTryIncome = nowTryIncome
    if nowTryIncome > lastTryIncome:
        lastTryIncome = nowTryIncome
        succeed = True

    return json.loads(str)
