#!/usr/bin/python
# -*-coding:utf-8-*-
import os
import sys

current_path = os.path.split(os.path.realpath(__file__))[0]
module_path = current_path[:current_path.rfind('/')]
print(module_path)

sys.path.insert(0, module_path)

import json
import time
from myutils import *

headers = {
    'Cookie': 'aliyungf_tc=AQAAABnMrwx1RgQABoSZtF8IrlKTFD2Y; gaoshou_session=eyJpdiI6Imd6VzczZ0FQVzhXdVZzQkpYZ2orYWc9PSIsInZhbHVlIjoiRk8xRTZ0MDYyVnlybElQNVhhbzJ6NjdJbjFsUU5LK3hzMVJtVHJkTmt2TElTdU5WOFdsMFwvV1RjdEE5bUlWNEFpSE54Q2hZUlk3bE13QVZvMXowQXdnPT0iLCJtYWMiOiIzNzc5ODJmZGM2NGQwMjdjMDhhNWQzNmY2MzA2YzIwZDE0MTIzMzc5M2E0YmE1MTYxMTE4OGM1MGMyYzE5NmI5In0%3D; PHPSESSID=a7ae13340da937d4931e583e9409abc0f5021f47; qk_app_id=13; qk_ll=eyJpdiI6IjdlOU1qRWErVktHZExcL0xRdlhkY293PT0iLCJ2YWx1ZSI6InltemxIN1NuK0FZOE5RZ29Qdm4xWWc9PSIsIm1hYyI6ImZjZmQ0YzY0MmFlOGIzNTI5NDQzNjFhMDRkMmUyNmI5NTFiMzg5NWZmNTk0YTBhOGYwODY0Zjg5ZTBiZmJiYjAifQ%3D%3D; qk:guid=bd86a9c0-b3c0-11e5-8b24-cdc5e0ec6fea-20160105',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": 'zh-cn',
    "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
    "Connection": 'keep-alive',
    "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
}


# 构建参数
def params(adid, adname):
    userid = '32483806'
    dict = {
        'adid': adid,
        'adname': adname,
        'check_click': '0',
        'deviceid': '5268855F-AA59-4BFE-B64F-61D04F19DE3C',
        'dsid': '382080527',
        'mdt': '474546411',
        'order': userid + adid,
        'rdl': '0',
        'time': '%d' % (int(time.time())),
        'ver': '1144.17'
    }

    keys = ['adid', 'adname', 'check_click', 'deviceid', 'dsid', 'mdt', 'order', 'rdl', 'time', 'ver']
    # keys.reverse()

    sign = ""
    for key in keys:
        sign += key + '=' + dict[key]

    sign += '7c64d964f0e544d8826ea5234338fc0e'
    m = hashlib.md5()
    m.update(sign.encode('utf-8'))
    sign = m.hexdigest()

    dict['sign'] = sign

    print('sign', sign)

    # 拼装url参数
    urlparam = ''
    for k in dict.keys():
        if k == 'adname':
            dict[k] = urllib.quote_plus(dict[k].encode('utf-8'))
        urlparam += k + '=' + dict[k] + '&'

    urlparam = urlparam[:-1]

    print('urlparam', urlparam)

    return urlparam


# 抓取任务
def fetchTask():
    url = 'http://m.qianka.com/api/h5/subtask/fetch'
    conn = httplib.HTTPConnection("m.qianka.com")
    conn.request(method='GET', url=url, headers=headers)
    response = conn.getresponse()
    status = response.status
    print("fetch status: %d  t:%d" % (status, time.time()))

    while status != 200:
        print("fetch retry")
        conn = httplib.HTTPConnection("m.qianka.com")
        conn.request(method='GET', url=url, headers=headers)
        response = conn.getresponse()
        status = response.status

    resp = response.read()
    # if type(resp)==type('a'):
    resp = resp.decode('unicode-escape')
    tasklist = json.loads(resp)['data']

    # print("tasklist: %s" % str(tasklist).decode('unicode-escape'))

    availableTasks = []
    for task in tasklist:
        # 筛选进行中的任务
        if task['type'] == 1 and task['qty'] > 0 and task['status_order'] == 2 and task['status'] == 1:
            availableTasks.append(task)

    print("availableTasks: %s" % availableTasks)

    # 排序
    if len(availableTasks) > 1:
        availableTasks.sort(key=lambda x: int(x['qty']))

    conn.close()

    return availableTasks


# 抢任务
def start_v2(task):
    # 1. 抢任务
    url = 'http://m.qianka.com/api/h5/subtask/start_v2'
    conn = httplib.HTTPConnection("m.qianka.com")
    conn.request(method='POST', url=url, headers=headers, body='{"task_id":%d}' % task['id'])
    response = conn.getresponse()
    status = response.status
    print("start_v2 status: %d" % status)

    while status != 200:
        print("start_v2 retry")
        conn = httplib.HTTPConnection("m.qianka.com")
        conn.request(method='POST', url=url, headers=headers, body='{"task_id":%d}' % task['id'])
        response = conn.getresponse()
        status = response.status

    resp = response.read().decode('unicode-escape')

    try:
        print("start_v2 resp:%s" % resp)
    except Exception,e :
        print(e)

    return json.loads(resp)['data']


# 上传app下载状态
def uploadAppStatus(adid, adname):
    url = 'http://gaos.guo7.com/zq_api/index.php/lianmeng/ziji?%s' % params(adid, adname)
    conn = httplib.HTTPConnection("gaos.guo7.com")
    _headers = {
        'Accept': '*/*',
        'Cookie': 'aliyungf_tc=AQAAACCfSzEYdQEAS0Xhevm8qhYtsk0J',
        'User-Agent': 'QiankaKey/2.0 (iPhone; iOS 8.3; Scale/2.00)',
        'Accept-Language': 'zh-Hans;q=1',
        # 'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'

    }
    conn.request(method='GET', url=url, headers=_headers)
    response = conn.getresponse()
    status = response.status
    print("uploadAppStatus status: %d" % status)

    while status != 200:
        print("fetch retry")
        conn = httplib.HTTPConnection("m.qianka.com")
        conn.request(method='GET', url=url, headers=_headers)
        response = conn.getresponse()
        status = response.status

    try:
        print("uploadAppStatus resp:%s" % response.read().decode('unicode-escape'))
    except Exception,e:
        print(e)


# 执行任务
def completeTask(tasklist):
    # if len(tasklist)>0:
    #     setting()
    #     day_journals()
    for task in tasklist:
        if start_v2(task)['type'] == 1 and start_v2(task)['type'] == 2:
            # succeed
            print("start_v2 ok")

            # getoneself_info
            task_id = str(task['id'])
            # getoneself_info(task_id)

            # 上传app下载状态
            uploadAppStatus(task_id, task['title'])


# setting
def setting():
    print(http_retry(
        "http://api.guo7.com/setting.php?app=qk_key_1_16-13&bundleid=com.sws.app&channel=3&idfa=5268855F-AA59-4BFE-B64F-61D04F19DE3C&uuid=15CECF34-57F1-41A9-9740-477DA0A7C95B&version=2.0"))


def day_journals():
    content = """
        batteryCapacityLeft	95
        bssid	58:ac:78:eb:7b:5f
        bundleid	com.sws.app
        carrier	中国联通
        device	iPhone 5s (Global)
        deviceID	7105089584816
        freeDiskspace	1763
        idfa	5268855F-AA59-4BFE-B64F-61D04F19DE3C
        isBatteryCharging	1
        isBatteryPluggedIn	1
        jailbroken	0
        localIP	172.24.104.98
        localMAC	02:00:00:00:00:00
        model	iPhone 5s (Global)
        networkStatus	5
        open_num	9
        openudid	990781d14810f1f2317fe9f3171a5c323ed937e7
        operating_system	8.3
        push	1
        resolution_ratio	640x1136
        screenBrightness	0.11074148863554
        ssid	DP
        system	8.3
        systemOpenTime	1449538706
        systemRunningTime	525.603743628669
        timestamp	1452849015.121978
        totalDiskspace	12305
        uuid	15CECF34-57F1-41A9-9740-477DA0A7C95B
        version	2.0.2015122101

    """

    resp = http_retry('http://gaos.guo7.com/zq_api/api/day_journals', method='POST',
                      headers=headers_from_str("""
                        Content-Type: application/x-www-form-urlencoded
                        Connection: keep-alive
                        Accept: */*
                        User-Agent: QiankaKey/2.0 (iPhone; iOS 8.3; Scale/2.00)
                        Accept-Language: zh-Hans;q=1

                        """), body=params2(content, ))

    print('day_journals resp:%s' % resp.decode('unicode-escape'))


# getoneself_info 参数获取
def params2(contentStr, data={}):
    key = 'aa57592108800bdf'  # 很不容算出来的,二次密钥为 LJR1AmH5ZwRjBQtjZTWxMt==

    __dict = {}
    dict_keys = []
    for line in contentStr.split('\n'):
        arr = line.split('\t')
        if len(arr) == 2:
            k = arr[0].strip()
            v = arr[1].strip()
            dict_keys.append(k)
            __dict[k] = v

    __dict['timestamp'] = str(time.time())

    for sk in data.keys():
        __dict[sk] = data[sk]

    # 计算签名
    content = ""
    for kk in dict_keys:
        content += kk + '=' + __dict[kk] + '+'

    content = content[:-1] + key
    m = hashlib.md5()
    m.update(content)
    sign = m.hexdigest()
    __dict['sig'] = sign

    print('params2 sign:%s' % sign)

    # 拼装url参数
    # urlparam =urllib.urlencode(dict)
    dict_keys.insert(dict_keys.index('ssid'), 'sig')
    urlparam = ''
    for ks in dict_keys:
        urlparam += ks + '=' + urllib.quote_plus(__dict[ks]).replace('+', '%20') + '&'
        # urlparam += ks + '=' + __dict[ks] + '&'

    urlparam = urlparam[:-1]

    print('params2 urlparam:%s' % urlparam)

    return urlparam


def getoneself_info(task_id):
    content = params2("""
                batteryCapacityLeft	46
                bssid	cc:46:d6:26:bc:6f
                bundleid	com.sws.app
                carrier	中国联通
                deviceID	7105089584816
                freeDiskspace	2230
                idfa	5268855F-AA59-4BFE-B64F-61D04F19DE3C
                isBatteryCharging	0
                isBatteryPluggedIn	0
                jailbroken	0
                localIP	172.24.110.144
                localMAC	02:00:00:00:00:00
                model	iPhone 5s (Global)
                networkStatus	5
                openudid	990781d14810f1f2317fe9f3171a5c323ed937e7
                push	1
                screenBrightness	0.1642156839370728
                ssid	DP
                system	8.3
                systemOpenTime	1449538706
                systemRunningTime	360.0351954686112
                task_id	123477
                timestamp	1452062787.439038
                totalDiskspace	12305
                uuid	15CECF34-57F1-41A9-9740-477DA0A7C95B
                version	2.0.2015122101

                """, data={'task_id': task_id})

    h = headers_from_str("""
        Content-Type: application/x-www-form-urlencoded
        Accept: */*
        Connection: keep-alive
        Cookie: aliyungf_tc=AQAAACCfSzEYdQEAS0Xhevm8qhYtsk0J
        User-Agent: QiankaKey/2.0 (iPhone; iOS 8.3; Scale/2.00)
        Accept-Language: zh-Hans;q=1
    """)

    resp = http_retry("http://gaos.guo7.com/zq_api/api/getoneself_info", method='POST', headers=h, body=content)

    print('getoneself_info resp:%s' % resp.decode('unicode-escape'))


#
if __name__ == '__main__':

    for i in range(29):
        completeTask(fetchTask())
        time.sleep(2)


# getoneself_info('123477')

# day_journals()

# print(params('124131','掌上电玩城'))


# fetchTask()
# setting()
# uploadAppStatus('124266',u'天天暴走')

# ss=u'\u8bbe\u5907\u7c7b\u578b\u9519\u8bef'
#
# print(type(ss))
# #
# # # ss=unicode(ss,'utf-8')
# # ss=ss.decode('ascii').encode('utf-8')
# #
# ss=ss.decode('unicode-escape')
#

# ss=ss.decode('unicode-escape')
# print(ss)
