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

headers = {
    'Cookie': 'Hm_lpvt_55a5855402d9f76f9739ffa75d37dfb2=1452391236; Hm_lvt_55a5855402d9f76f9739ffa75d37dfb2=1452334485,1452354788,1452355989,1452391203; OD=Olo0qpP2ElhpNGWckUiiypH4hQKMrRLKJJPAKQDG7giNe1A5gKj79A7LiAZtTPIK; JSESSIONID=BDEEB06418C807A76831269C923FE0B1; SERVERID=ec0dc4249f8af0df85b70311bff7ff5c|1452391297|1452388835',
    "Accept": "text/plain, */*; q=0.01",
    # "X-Requested-With": 'XMLHttpRequest',
    "Accept-Encoding": 'gzip, deflate',
    "Accept-Language": 'zh-cn',
    "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
    # "Origin": 'http://itry.com',
    "Connection": 'keep-alive',
    "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
}

user_id = 16973020


def sortApplist(list):
    if len(list) > 1:
        list.sort(key=lambda x: int(x['order_status_disp']))

    return list


def completeTask():
    # 1. 获取app列表
    resp = urllib.urlopen("http://itry.com/shike/getApplist/16973020/CBED9F24D48D24964B7B87BCD6AE8FF4").read()
    print(resp)
    for app in sortApplist(json.loads(resp)):
        if app['order_status_disp'] != '0':
            # 可以下载
            xb_online()
            # print(app['search_word'])

            appid = app['appid']
            order_id = app['order_id']
            bundle_id = app['bundle_id'].encode("UTF-8")
            process_name = app['process_name'].encode("UTF-8")

            # 点击并且复制关键词
            content = "appid=%s&user_id=16973020&order_Id=%s&type=app" % (appid, order_id)

            # 2.点击纪录
            url = 'http://itry.com/shike/user_click_record'
            conn = httplib.HTTPConnection("itry.com")
            conn.request(method='POST', url=url, body=content, headers=headers)
            response = conn.getresponse()
            text = response.read()
            print(response.status)
            print(text)
            conn.close()

            if text != '0':
                print("没抢到,库存可能不够,直接下一个")
                continue

            printAppStatus(bundle_id, process_name)

            # 3.复制关键词
            url = 'http://itry.com/shike/copy_keyword'
            conn = httplib.HTTPConnection("itry.com")
            conn.request(method='POST', url=url, body=content, headers=headers)
            response = conn.getresponse()
            text = response.read()
            print(response.status)
            print(text)
            conn.close()

            while text != '0':
                print("没抢到,重试")
                url = 'http://itry.com/shike/copy_keyword'
                conn = httplib.HTTPConnection("itry.com")
                conn.request(method='POST', url=url, body=content, headers=headers)
                response = conn.getresponse()
                text = response.read()
                print(response.status)
                print(text)
                conn.close()

            printAppStatus(bundle_id, process_name)

            # 4.模拟下载并打开应用
            fakeDownAndOpenApp(appid, bundle_id, process_name)

            # break

    else:
        open('/data/code/python_penkie/apps/sync.txt', 'w').write('0')


def xb_online():
    content = 'user_id=16973020&status=0'
    content = 'p=' + encryptContent(content)
    url = 'http://xb.itry.com/xb_online'
    conn = httplib.HTTPConnection("xb.itry.com")
    headers['User-Agent'] = 'com.delianda.dongxiang/1.19 CFNetwork/711.3.18 Darwin/14.0.0'
    conn.request(method='POST', url=url, body=content, headers=headers)
    response = conn.getresponse()
    print(response.status)
    print(response.read())
    conn.close()


def json_time(bundle_id, process_name, content):
    url = 'http://xb.itry.com/json_time'
    conn = httplib.HTTPConnection("xb.itry.com")
    headers['User-Agent'] = 'com.delianda.dongxiang/1.19 CFNetwork/711.3.18 Darwin/14.0.0'
    conn.request(method='POST', url=url, body=content, headers=headers)
    response = conn.getresponse()
    text = response.read()
    print(response.status)
    print(text)
    conn.close()
    if response.status != 200:
        json_time(bundle_id, process_name, content)
    printAppStatus(bundle_id, process_name)


def fakeDownAndOpenApp(appid, bundle_id, process_name):
    # 更新sync.txt 防止job拥堵
    open('/data/code/python_penkie/apps/sync.txt', 'w').write('1')

    getUserFinance()
    # 下载中
    content = 'user_id=16973020&idfa=&bs=635443433373543323144464856344344000000000000010000010000000100&cc=340&app=(null),%s,%s,473522972,0,0,0,(null)%s16973020&ver=1.19&type=d_package' % (
        appid, bundle_id, '%7C%7C')
    content = 'p=' + encryptContent(content, 0)
    json_time(bundle_id, process_name, content)

    # 下载完成
    content = 'user_id=16973020&idfa=&bs=635443433373543323144464856344344000000000000010000010000000100&cc=340&app=382080527,%s,%s,473523166,0,143465,1,2.110.0%s16973020&ver=1.19&type=d_package' % (
        appid, bundle_id, '%7C%7C')
    content = 'p=' + encryptContent(content, 0)
    json_time(bundle_id, process_name, content)

    # 每隔1分钟上传进程状态
    for i in range(30):
        uploadProcessStatus(bundle_id, process_name)
        global succeed
        if succeed:
            print("completed!")
            succeed = False
            break
        time.sleep(10)


def uploadProcessStatus(bundle_id, process_name):
    content = 'user_id=16973020&bs=635443433373543323144464856344344000000000000010000010000000100&cc=340&idfa=5268855F-AA59-4BFE-B64F-61D04F19DE3C&idfv=EE9251DE-E401-4340-BA4E-2A3171B1C480&uid=3c2e3d88ea4c7a407c08d5714bd13e3eaf0a3d74&mac=80:89:17:87:49:92&usb=46.000000&app=launchd,2291948.993783,16390||CVMServer,606019.996496,16388||WeChat,3516.999015,16388||BDPhoneBrowser,3051.999252,16388||SafariCloudHisto,2734.999395,16388||dongxiang,2666.999904,16388||nanoregistryd,2609.000210,16388||nanoregistrylaun,2602.000325,16388||MobileNotes,1869.001144,16388||QQ,375.002563,16388||carkitd,363.002657,16388||com.apple.WebKit,324.002822,16388||com.apple.WebKit,324.002923,16388||%s,242.003093,16388||&ver=1.19&type=d_process' % (
        process_name)
    content = 'p=' + encryptContent(content)
    json_time(bundle_id, process_name, content)

    getUserFinance()


def printAppStatus(bundle_id, process_name):
    print(urllib.urlopen('http://itry.com/shike/getAppStatus/%s/16973020/%s' % (bundle_id, process_name)).read())


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


def getUserFinance():
    url = 'http://itry.com/itry/income/getUserFinance'
    content = 'openidMD5=CBED9F24D48D24964B7B87BCD6AE8FF4&cur_time=%d' % (datetime.datetime.now().microsecond)
    conn = httplib.HTTPConnection("itry.com")
    conn.request(method='POST', url=url, body=content, headers=headers)
    response = conn.getresponse()
    print(response.status)

    if response.status == 200:
        str = response.read()
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

        conn.close()
        return json.loads(str)


def check_sync():
    # 检查是否有进行中的任务
    return open('/data/code/python_penkie/apps/sync.txt').read().strip() == '0'


if __name__ == '__main__':
    # open('sync.txt', 'w').write('1')
    if check_sync():
        completeTask()
    else:
        print("doing")
        # time.sleep(1)
#
# appid = '953061503'
# bundid = 'com.koudailicai.R'
# processname = 'KDLC'
#
# printAppStatus(bundid, processname)
# xb_online()
# fakeDownAndOpenApp(appid, bundid, processname)
#
# getUserFinance()


# str=u"""
# [{
# 	"appid": 368677368,
# 	"name": "优步Uber ---- 全球领先的打车软件",
# 	"icon": "http://is3.mzstatic.com/image/thumb/Purple7/v4/6a/9d/65/6a9d659f-38bb-defd-3eec-6006c863684a/source/512x512bb.jpg",
# 	"price": null,
# 	"version": null,
# 	"bundle_id": "com.ubercab.UberClient",
# 	"file_size_bytes": 6.0109019E7,
# 	"devices": 0,
# 	"package_name": null,
# 	"c_time": null,
# 	"type_name": "旅游",
# 	"u_time": null,
# 	"details_url": "/shike/appDetails/368677368/38364/CBED9F24D48D24964B7B87BCD6AE8FF4",
# 	"order_id": 38364,
# 	"status": "0",
# 	"subhead": "前台打开,试玩5分钟",
# 	"search_word": "专车",
# 	"down_price": 2.00,
# 	"ranking": 1,
# 	"app_desc": null,
# 	"play_url": null,
# 	"publisher_wx_gzh": null,
# 	"order_number": 16000,
# 	"complete_number": 7673,
# 	"click_number": 8818,
# 	"under_number": 16000,
# 	"e_time": "2016-01-03 22:59:00.0",
# 	"order_status_disp": "7182",
# 	"btnStatus_disp": null,
# 	"leaveStatusPic": "remaining_amount",
# 	"order_status_disp_play": null,
# 	"typepicDisp": null,
# 	"review_money": null,
# 	"moneyDisp": null,
# 	"s_time": "2016-01-03 22:06:37.0",
# 	"shike_id": null,
# 	"process_name": "UberClient",
# 	"l_id": 0,
# 	"r_id": 0,
# 	"cn": 0,
# 	"play_banner_path": null
# }, {
# 	"appid": 487608658,
# 	"name": "QQ阅读-小说电子书阅读器",
# 	"icon": "http://is4.mzstatic.com/image/thumb/Purple69/v4/fd/35/2e/fd352ea1-9238-cabd-288e-4c1d7b3c3c54/source/512x512bb.jpg",
# 	"price": null,
# 	"version": null,
# 	"bundle_id": "com.tencent.qqreaderiphone",
# 	"file_size_bytes": 3.6476559E7,
# 	"devices": 0,
# 	"package_name": null,
# 	"c_time": null,
# 	"type_name": "图书",
# 	"u_time": null,
# 	"details_url": "/shike/appDetails/487608658/38998/CBED9F24D48D24964B7B87BCD6AE8FF4",
# 	"order_id": 38998,
# 	"status": "8",
# 	"subhead": "前台打开,试玩5分钟",
# 	"search_word": "芈月传小说",
# 	"down_price": 2.00,
# 	"ranking": 2,
# 	"app_desc": null,
# 	"play_url": null,
# 	"publisher_wx_gzh": null,
# 	"order_number": 1000,
# 	"complete_number": 951,
# 	"click_number": 1000,
# 	"under_number": 1000,
# 	"e_time": "2016-01-03 23:50:00.0",
# 	"order_status_disp": "0",
# 	"btnStatus_disp": null,
# 	"leaveStatusPic": "remaining_amount",
# 	"order_status_disp_play": null,
# 	"typepicDisp": null,
# 	"review_money": null,
# 	"moneyDisp": null,
# 	"s_time": "2016-01-03 19:20:00.0",
# 	"shike_id": null,
# 	"process_name": "QQReaderUI",
# 	"l_id": 0,
# 	"r_id": 0,
# 	"cn": 0,
# 	"play_banner_path": null
# }, {
# 	"appid": 923920872,
# 	"name": "平安好医生-计步赚钱每天6元，全职医生免费看病",
# 	"icon": "http://is4.mzstatic.com/image/thumb/Purple4/v4/c1/cf/99/c1cf992b-14af-a9bd-1033-b02416dd8c7e/source/512x512bb.jpg",
# 	"price": null,
# 	"version": null,
# 	"bundle_id": "com.pajk.personaldoctor",
# 	"file_size_bytes": 4.9334504E7,
# 	"devices": 0,
# 	"package_name": null,
# 	"c_time": null,
# 	"type_name": "医疗",
# 	"u_time": null,
# 	"details_url": "/shike/appDetails/923920872/38227/CBED9F24D48D24964B7B87BCD6AE8FF4",
# 	"order_id": 38227,
# 	"status": "8",
# 	"subhead": "前台打开,试玩5分钟",
# 	"search_word": "计步",
# 	"down_price": 2.00,
# 	"ranking": 1,
# 	"app_desc": null,
# 	"play_url": null,
# 	"publisher_wx_gzh": null,
# 	"order_number": 5000,
# 	"complete_number": 4809,
# 	"click_number": 5001,
# 	"under_number": 5000,
# 	"e_time": "2016-01-03 23:30:00.0",
# 	"order_status_disp": "0",
# 	"btnStatus_disp": null,
# 	"leaveStatusPic": "remaining_amount",
# 	"order_status_disp_play": null,
# 	"typepicDisp": null,
# 	"review_money": null,
# 	"moneyDisp": null,
# 	"s_time": "2016-01-03 20:00:00.0",
# 	"shike_id": null,
# 	"process_name": "PAPersonalDoctor",
# 	"l_id": 0,
# 	"r_id": 0,
# 	"cn": 0,
# 	"play_banner_path": null
# }, {
# 	"appid": 486744917,
# 	"name": "国美在线 - 家电，特卖，热门团购，正品优惠",
# 	"icon": "http://is3.mzstatic.com/image/thumb/Purple69/v4/cc/05/40/cc0540be-bf73-e6a3-859b-24bf6c69de75/source/512x512bb.jpg",
# 	"price": null,
# 	"version": null,
# 	"bundle_id": "com.gome.gomeEShop",
# 	"file_size_bytes": 6.2125961E7,
# 	"devices": 0,
# 	"package_name": null,
# 	"c_time": null,
# 	"type_name": "购物",
# 	"u_time": null,
# 	"details_url": "/shike/appDetails/486744917/37656/CBED9F24D48D24964B7B87BCD6AE8FF4",
# 	"order_id": 37656,
# 	"status": "8",
# 	"subhead": "前台打开,试玩5分钟",
# 	"search_word": "中粮",
# 	"down_price": 2.00,
# 	"ranking": 1,
# 	"app_desc": null,
# 	"play_url": null,
# 	"publisher_wx_gzh": null,
# 	"order_number": 500,
# 	"complete_number": 78,
# 	"click_number": 290,
# 	"under_number": 500,
# 	"e_time": "2016-01-03 23:30:00.0",
# 	"order_status_disp": "210",
# 	"btnStatus_disp": null,
# 	"leaveStatusPic": "remaining_amount",
# 	"order_status_disp_play": null,
# 	"typepicDisp": null,
# 	"review_money": null,
# 	"moneyDisp": null,
# 	"s_time": "2016-01-03 22:00:00.0",
# 	"shike_id": null,
# 	"process_name": "GomeEShop",
# 	"l_id": 0,
# 	"r_id": 0,
# 	"cn": 0,
# 	"play_banner_path": null
# }]
# """
#
#
# print(sortApplist(json.loads(str)))