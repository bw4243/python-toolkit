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
    'Cookie': 'Hm_lvt_55a5855402d9f76f9739ffa75d37dfb2=1452505832,1452515643,1452529063,1452614927; OD=fSTxC/hYV33V+qPULOZ4SW3Hv0yxHFzZrLR+SC4T2tALdWFC2pf1oYnL5/CxuA0x; JSESSIONID=7D11114C8D3D092047BA0BF40B7DDC2D; SERVERID=68eb2ae2fa25dc0af715a6507d823a0b|1452693600|1452693600',
    "Accept": "text/plain, */*; q=0.01",
    # "X-Requested-With": 'XMLHttpRequest',
    "Accept-Encoding": 'gzip, deflate',
    "Accept-Language": 'zh-cn',
    "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
    # "Origin": 'http://itry.com',
    "Connection": 'keep-alive',
    "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
}

user_id = 16715527

isEmpty=False
def sortApplist(list):
    if len(list) > 1:
       list.sort(key=lambda x: int(x['order_status_disp']))

    return list


def completeTask():
    # 1. 获取app列表
    fs = urllib.urlopen("http://itry.com/shike/getApplist/16715527/6B758696931041EC015EB9127851876F")
    print(fs.code)
    resp = fs.read()
    print(resp)

    while fs.code != 200:
        fs = urllib.urlopen("http://itry.com/shike/getApplist/16715527/6B758696931041EC015EB9127851876F")
        resp = fs.read()
        print(fs.code)
        print(resp)

    list=json.loads(resp)

    for app in sortApplist(list):
        if app['order_status_disp'] != '0':
            # 可以下载
            xb_online()
            # print(app['search_word'])

            appid = app['appid']
            order_id = app['order_id']
            bundle_id = app['bundle_id'].encode("UTF-8")
            process_name = app['process_name'].encode("UTF-8")

            # 点击并且复制关键词
            content = "appid=%s&user_id=16715527&order_Id=%s&type=app" % (appid, order_id)

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
        open('/data/code/python_penkie/apps/sync_cjj.txt', 'w').write('0')


def xb_online():
    content = 'user_id=16715527&status=0'
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
    # 更新sync_cjj.txt 防止job拥堵
    open('/data/code/python_penkie/apps/sync_cjj.txt', 'w').write('1')

    getUserFinance()
    # 下载中
    content = 'user_id=16715527&idfa=&bs=F5D545302WJG5NYA3&cc=15&app=(null),%s,%s,473522972,0,0,0,(null)%s16715527&ver=1.19&type=d_package' % (
        appid, bundle_id, '%7C%7C')
    content = 'p=' + encryptContent(content, 0)
    json_time(bundle_id, process_name, content)

    # 下载完成
    content = 'user_id=16715527&idfa=&bs=F5D545302WJG5NYA3&cc=15&app=382080529,%s,%s,473523166,0,143465,1,2.110.0%s16715527&ver=1.19&type=d_package' % (
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
    content = 'user_id=16715527&bs=F5D545302WJG5NYA3&cc=15&idfa=7E48C310-7260-4E65-AD76-7180422A2214&idfv=84AC9200-69F7-4437-B91B-4CA0839ECF79&uid=d41d8cd98f00b204e9800998ecf8427e2af0c2f8&mac=80:89:17:87:49:92&usb=27.000002&app=launchd,2291948.993783,16390||CVMServer,606019.996496,16388||WeChat,3516.999015,16388||BDPhoneBrowser,3051.999252,16388||SafariCloudHisto,2734.999395,16388||dongxiang,2666.999904,16388||nanoregistryd,2609.000210,16388||nanoregistrylaun,2602.000325,16388||MobileNotes,1869.001144,16388||QQ,375.002563,16388||carkitd,363.002657,16388||com.apple.WebKit,324.002822,16388||com.apple.WebKit,324.002923,16388||%s,242.003093,16388||&ver=1.19&type=d_process' % (
        process_name)
    content = 'p=' + encryptContent(content)
    json_time(bundle_id, process_name, content)

    getUserFinance()


def printAppStatus(bundle_id, process_name):
    print(urllib.urlopen('http://itry.com/shike/getAppStatus/%s/16715527/%s' % (bundle_id, process_name)).read())


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
    content = 'openidMD5=6B758696931041EC015EB9127851876F&cur_time=%d' % (datetime.datetime.now().microsecond)
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
    return open('/data/code/python_penkie/apps/sync_cjj.txt').read().strip() == '0'


if __name__ == '__main__':
    # open('sync_cjj.txt', 'w').write('1')
    # for i in range(10):
    if check_sync():
        completeTask()
    else:
        print("doing")
        # time.sleep(3)
