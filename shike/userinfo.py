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
from moneydb.models import User
from myutils import *
from moneydb import db
import taskrunner
from moneydb.constants import *


def get_header(cookie):
    return {
        'Cookie': cookie,
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": 'zh-cn',
        "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
        "Connection": 'keep-alive',
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
    }


def get_user_finance(user):
    """
    查询用户财务信息
    :param user:
    :return:
    """

    url = 'http://i.appshike.com/itry/income/getUserFinance'
    content = 'openidMD5=%s&cur_time=%d' % (user.oid_md5, datetime.datetime.now().microsecond)

    resp = http_retry(url, method='POST', body=content, headers=get_header(user.cookie))

    obj = json.loads(resp)
    # print(response.read())
    # print('今日收入:%s' % obj['today_income'].encode('UTF-8'))

    for k, v in obj.items():
        if v and u'元' in v:
            obj[k] = float(v.encode('UTF-8')[:-3])

    return obj


def has_money_up(user):
    """
    余额是否增长了
    :return: True/False
    """
    finance = get_user_finance(user)
    if finance['history_income'] > user.total_income:
        # 钱加上去了
        user.total_income = finance['history_income']
        return True
    return False


def sync_user_info(user):
    """
    同步用户基本信息 ,如 余额,收入等
    :param user:
    :return:
    """
    finance = get_user_finance(user)
    s = db.session()
    s.query(User).filter(User.id == user.id).update({
        User.balance: finance['can_withdrawal'],
        User.total_income: finance['history_income'],
        User.today_income: finance['today_income'],
        User.freeze_status: finance['user_status']
    })
    s.commit()
    s.close()


def bind_info(user):
    content = 'user_id=%s&oid_md5=%s&binding=17_1&idfa=%s&idfv=%s&uid=%s&sn=no&bs=F5D545302WJG5NYA3&cc=340&dm=iPhone7,2&sv=8.1.2&ot=-27144&mac=&rm=cc:46:d6:26:bc:6f&ri=172.24.125.213&dt=(null)&ut=453&ls=12988858368&pn=18&ver=1.19&rn=DP' \
              % (user.user_id, user.oid_md5, user.idfa, user.idfv, user.uid)
    taskrunner.json_time(str(content), url='http://xb.appshike.com/json')

    content = 'user_id=%s&idfa=&bs=F5D545302WJG5NYA3&cc=340&app=1611445442,333206289,com.alipay.iphoneclient,474278250,0,143465,1,9.5.1%s1611445442,425349261,com.netease.news,474534964,0,143465,1,474%s(null),0,com.sogou.sogouinput,454115166,0,0,1,3.0.0' \
              % (user.user_id,  '%7C%7C', '%7C%7C')
    # content='user_id=18293475&idfa=&bs=F5D439168VZFW5TBS&cc=130&app=1611445442,333206289,com.alipay.iphoneclient,474278250,0,143465,1,9.5.1%7c%7c1611445442,425349261,com.netease.news,474534964,0,143465,1,474%7c%7c(null),0,com.sogou.sogouinput,454115166,0,0,1,3.0.0'
    taskrunner.json_time(str(content),replace=1)

    content = 'user_id=%s&idfa=&bs=F5D439168VZFW5TBS&cc=130&app=847712612,350962117,com.sina.weibo,453928544,0,143465,1,5.3.0%s10037034958,547166701,com.baidu.netdisk,475503388,0,143465,1,6.9.4%s(null),0,com.gad.shiliu,475550728,0,0,1,1.19' \
              % (user.user_id, '%7C%7C', '%7C%7C')
    taskrunner.json_time(str(content),replace=1)

    content = 'user_id=%s&bs=F5D439168VZFW5TBS&cc=130&idfa=%s&idfv=%s&uid=%s&mac=cc:46:d6:26:bc:6f&usb=28.000000&app=launchd,112685.932940,16390||nfcd,112673.934593,16388||WeChat,98017.934869,16388||eapolclient,167.936738,16644||com.apple.WebKit,62.936910,16388||com.apple.WebKit,62.936985,16388||com.apple.WebKit,61.937043,16388||com.apple.WebKit,40.937272,16388||shiliu,8.937662,16388||com.apple.WebKit,0.937784,16388||&ver=1.19&type=d_process' \
              % (user.user_id, user.idfa, user.idfv, user.uid)
    taskrunner.json_time(str(content))


def add_user():
    user = User(
        user_id='16715527',
        nick_name=u'晶晶',
        cookie='Hm_lvt_55a5855402d9f76f9739ffa75d37dfb2=1452505832,1452515643,1452529063,1452614927; OD=fSTxC/hYV33V+qPULOZ4SW3Hv0yxHFzZrLR+SC4T2tALdWFC2pf1oYnL5/CxuA0x; JSESSIONID=7D11114C8D3D092047BA0BF40B7DDC2D; SERVERID=68eb2ae2fa25dc0af715a6507d823a0b|1452693600|1452693600',
        oid_md5='6B758696931041EC015EB9127851876F',
        app_type=APP_TYPE_XIAO_BIN,
        idfa='7E48C310-7260-4E65-AD76-7180422A2214',  # gen_uuid(),
        idfv='84AC9200-69F7-4437-B91B-4CA0839ECF79',  # gen_uuid(),
        uid='d41d8cd98f00b204e9800998ecf8427e2af0c2f8',  # random_str(40)
    )
    db.add(user)

    # bind_info(user)


def log_download_xb(user):
    # 小妮子 {"rtn":1,"binding":"17_1"}
    logger.info(http_retry('http://i.appshike.com/itry/log_download_xb?oid_md5=%s' % user.oid_md5,
                           headers=get_header(user.cookie)))
