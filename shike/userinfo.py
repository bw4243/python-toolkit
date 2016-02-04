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
    log_download_xb(user)

    content = 'user_id=%s&oid_md5=%s&binding=18_1&idfa=%s&idfv=%s&uid=%s&sn=no&bs=F5D545202WJG5NZA4&cc=120&dm=iPhone8,2&sv=8.1.2&ot=-27144&mac=&rm=cc:42:d6:26:bc:6f&ri=132.24.125.213&dt=(null)&ut=452&ls=12988858322&pn=18&ver=1.19&rn=DP' \
              % (user.user_id, user.oid_md5, user.idfa, user.idfv, user.uid)
    taskrunner.json_time(str(content), url='http://xb.appshike.com/json')

    # content = 'user_id=%s&idfa=&bs=F5D545302WJG5NYA3&cc=340&app=1611445442,333206289,com.alipay.iphoneclient,474278250,0,143465,1,9.5.1%s1611445442,425349261,com.netease.news,474534964,0,143465,1,474%s(null),0,com.sogou.sogouinput,454115166,0,0,1,3.0.0' \
    #           % (user.user_id,  '%7C%7C', '%7C%7C')
    content = 'user_id=' + user.user_id + '&idfa=&bs=F5D545202WJG5NZA4&cc=120&app=1611445442,333206289,com.alipay.iphoneclient,474278250,0,143465,1,9.5.1%7C%7C1611445442,425349261,com.netease.news,474534964,0,143465,1,474%7C%7C(null),0,com.sogou.sogouinput,454115166,0,0,1,3.0.0%7C%7C(null),0,com.dianping.mp.mobile,471349340,0,0,1,4.1.0%7C%7C(null),0,com.google.chrome.ios,455139072,0,0,1,43.2357.51%7C%7C10037034958,351091731,com.dianping.dpscope,475571285,1,143465,1,8.0.0%7C%7C847712612,444934666,com.tencent.mqq,455195462,0,143465,1,5.6%7C%7C(null),0,com.dianping.apollo.crm,464783782,0,0,1,2.0.0.2%7C%7C(null),0,com.tongbu.tui.9675F56748,454500304,0,0,1,3.3.2%7C%7C(null),0,com.vstudio.PeakCamera,449226728,0,0,1,0.9.99%7C%7C1611445442,921478733,com.didapinche.taxi,475570075,0,143465,1,3.4.0%7C%7C' + user.user_id + '&ver=1.19&type=d_package'
    taskrunner.json_time(str(content), replace=1)

    content = 'user_id=' + user.user_id + '&idfa=&bs=F5D545202WJG5NZA4&cc=120&app=847712612,350962117,com.sina.weibo,453928544,0,143465,1,5.3.0%7C%7C10037034958,547166701,com.baidu.netdisk,475503388,0,143465,1,6.9.4%7C%7C(null),0,com.gad.shiliu,475550728,0,0,1,1.19%7C%7C1611445442,878534496,com.penglzh.Super12306,472454167,0,143465,1,2.0%7C%7C(null),0,com.tencent.eim,464636026,0,0,1,74557%7C%7C10037034958,414478124,com.tencent.xin,473205693,0,143465,1,6.3.9%7C%7C847712612,414245413,com.360buy.jdmobile,455462496,0,143465,1,22026%7C%7C' + user.user_id + '&ver=1.19&type=d_package'
    taskrunner.json_time(str(content), replace=1)

    content = 'user_id=%s&bs=F5D545202WJG5NZA4&cc=120&idfa=%s&idfv=%s&uid=%s&mac=cc:41:d6:26:bc:6f&usb=28.000000&app=launchd,112685.932940,16390||nfcd,112673.934593,16388||WeChat,98017.934869,16388||eapolclient,167.936738,16644||com.apple.WebKit,62.936910,16388||com.apple.WebKit,62.936985,16388||com.apple.WebKit,61.937043,16388||com.apple.WebKit,40.937272,16388||shiliu,8.937662,16388||com.apple.WebKit,0.937784,16388||&ver=1.19&type=d_process' \
              % (user.user_id, user.idfa, user.idfv, user.uid)
    taskrunner.json_time(str(content))


def add_user():
    user = User(
        user_id='18628202',
        nick_name=u'寻思',
        cookie='aliyungf_tc=AQAAADnttXVNFQkABoSZtLzl3vjjf0Wt; JSESSIONID=ACF5518874E853C25B4F706609C2D047; OD=6BYxG02tHVE2Arx0GsJd8eFL0Ga55PdZDPkUTOAbG+wf8o4yNI+d8ftZY+C2WwXx',
        oid_md5='22A02149EDAFBA184ED0A1A8AE6936E0',
        app_type=APP_TYPE_XIAO_BIN,
        idfa=gen_uuid(),
        idfv=gen_uuid(),
        uid=random_str(40)
    )
    db.add(user)

    # bind_info(user)


def log_download_xb(user):
    # 小妮子 {"rtn":1,"binding":"17_1"}
    logger.info(http_retry('http://i.appshike.com/itry/log_download_xb?oid_md5=%s' % user.oid_md5,
                           headers=get_header(user.cookie)))

