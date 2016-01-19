#!/usr/bin/python
# -*-coding:utf-8-*-
import time
from myutils import *
import json
from db import disciple


def bind_master(cookie, master_id):
    print(http_retry('http://m.qianka.com/api/h5/gift/first', headers={
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'}, method='POST', body='{"master_id":%s}' % master_id))


def home_index(cookie):
    print(http_retry('http://m.qianka.com/api/h5/home/index', headers=headers_from_str("""
        Host: m.qianka.com
        Accept: application/json, text/plain, */*
        Connection: keep-alive
        Cookie: %s
        User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4
        Accept-Language: zh-cn
        Referer: http://m.qianka.com/fe/dashboard/index.html?timestamp=1453093214978
    """ % cookie)).decode('unicode-escape'))


def login(idfa, uuid, userid):
    content = """
        batteryCapacityLeft	61
        bundleid	com.sws.app
        device	iPhone 5s (Global)
        freeDiskspace	1703
        idfa	%s
        isBatteryCharging	0
        isBatteryPluggedIn	0
        jailbroken	0
        localIP	192.168.1.102
        localMAC	02:00:00:00:00:00
        model	iPhone 5s (Global)
        networkStatus	5
        push	1
        screenBrightness	0.11074148863554
        systemOpenTime	1449538706
        systemRunningTime	549.2114206219444
        timestamp	1452957378.853804
        totalDiskspace	12305
        user_id\t%s
        uuid	%s
        version	2.0.2015122101
    """ % (idfa, userid, uuid)

    headers, resp = http_retry('http://x.qianka.com/assistant/weixin/login', method='POST',
                               headers=headers_from_str("""
                        Content-Type: application/x-www-form-urlencoded
                        Connection: keep-alive
                        Accept: */*
                        User-Agent: QiankaKey/2.0 (iPhone; iOS 8.3; Scale/2.00)
                        Accept-Language: zh-Hans;q=1

                        """), body=params2(content), return_headers=True)

    print(headers)
    print(resp)

    # 解析cookie
    cookie = ''
    for tp in headers:
        if tp[0] == 'set-cookie':
            cookie = tp[1].replace('Path=/; HttpOnly,', '').replace('path=/,', '')
            break
    return cookie


def reg_get_user():
    idfa = gen_uuid()
    uuid = gen_uuid()

    content = """
        batteryCapacityLeft	61
        bundleid	com.sws.app
        device	iPhone 5s (Global)
        freeDiskspace	1703
        idfa	%s
        isBatteryCharging	0
        isBatteryPluggedIn	0
        jailbroken	0
        localIP	192.168.1.102
        localMAC	02:00:00:00:00:00
        model	iPhone 5s (Global)
        networkStatus	5
        push	1
        screenBrightness	0.11074148863554
        systemOpenTime	1449538706
        systemRunningTime	549.2114206219444
        timestamp	1452957378.853804
        totalDiskspace	12305
        uuid	%s
        version	2.0.2015122101
    """ % (idfa, uuid)

    headers, resp = http_retry('http://gaos.guo7.com/zq_api/api/get_user', method='POST',
                               headers=headers_from_str("""
                                Content-Type: application/x-www-form-urlencoded
                                Connection: keep-alive
                                Accept: */*
                                User-Agent: QiankaKey/2.0 (iPhone; iOS 8.3; Scale/2.00)
                                Accept-Language: zh-Hans;q=1

                        """), body=params2(content), return_headers=True)
    #
    #
    # print(resp)
    #
    user_id = json.loads(resp)['id']

    cookie = login(idfa, uuid, user_id)

    return idfa, uuid, user_id, cookie


def get_uuid(idfa):
    content = """
        batteryCapacityLeft	61
        bundle_id	com.sws.app
        bundleid	com.sws.app
        freeDiskspace	1703
        idfa	%s
        isBatteryCharging	0
        isBatteryPluggedIn	0
        jailbroken	0
        localIP	192.168.1.102
        localMAC	02:00:00:00:00:00
        model	iPhone 5s (Global)
        networkStatus	5
        push	1
        screenBrightness	0.11074148863554
        system	8.3
        systemOpenTime	1449538706
        systemRunningTime	549.21151928772
        timestamp	1452957379.218191
        totalDiskspace	12305
        version	2.0.2015122101
    """ % idfa

    # content='idfa	5268855F-AA59-4BFE-B64F-61D04F19DE3C\nssid	zhouzhipeng\nuser_id	32483806\nuuid	15CECF34-57F1-41A9-9740-477DA0A7C95B'
    headers, resp = http_retry('http://gaos.guo7.com/zq_api/api/user_uuid', method='POST',
                               headers=headers_from_str("""
                                Content-Type: application/x-www-form-urlencoded
                                Connection: keep-alive
                                Accept: */*
                                User-Agent: QiankaKey/2.0 (iPhone; iOS 8.3; Scale/2.00)
                                Accept-Language: zh-Hans;q=1

                        """), body=params2(content), return_headers=True)

    print(headers)
    print(resp)


def day_journals():
    content = """
        batteryCapacityLeft	95
        bssid	58:ac:78:eb:7b:5f
        bundleid	com.sws.app
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

                        """), body=params2(content))

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

    if __dict['timestamp']:
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
    dict_keys.append('sig')
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


# 批量生产徒弟
def batch_gen():
    # 绑定master
    masters = ['32483806', '32515198']

    for master_id in masters:
        for i in range(100):
            idfa, uuid, user_id, cookie = reg_get_user()
            disciple.new_disciple(idfa, uuid, user_id, cookie)
            bind_master(cookie, master_id)

    print("===================>>>>>>>>>>")
    print(disciple.fetch_valid())


def alipay_withdraw(cookie, amount):
    print(http_retry('http://m.qianka.com/api/h5/exchange/doalipay', method='POST', headers=headers_from_str("""
        Accept: application/json, text/plain, */*
        Accept-Language: zh-cn
        Content-Type: application/json;charset=UTF-8
        Origin: http://m.qianka.com
        Connection: keep-alive
        User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4
        Cookie: %s
    """ % cookie), body='{"account":"18521058664","realname":"周志鹏","price":%d}' % amount).decode('unicode-escape'))


if __name__ == '__main__':
    # login()
    # add_user()
    # reg_get_user()
    # bind_master()
    cookie = 'aliyungf_tc=AQAAAHSRzEQXRwEABoSZtNrgiX1imW0r; gaoshou_session=eyJpdiI6IlFKREpQUkV5WGk2QkVnanNzUldqWXc9PSIsInZhbHVlIjoiakVYK1FtMnRIUlk4SUtzTXFJY0l1Y3FaTEVvZDlUNVVuME9LS0duVlpFaFZkQTFVdEdlcG9TYlNqWE94RzVJM2xiRFhaOWJYUU9iVVlZRDhVMnJ1U0E9PSIsIm1hYyI6ImE0MjZhM2I3N2IwYTQ5ZjBhODMzMWUzMzdiY2VlYjc1Mzc3MTI2MTljNTAzMzViNzU5NTFjMTE4ZDNmNjM2MTcifQ%3D%3D; PHPSESSID=bd7a1528e45d477fac27859f17bed60de9a53c5d; qk:guid=93e8deb0-bd9f-11e5-86c8-bbbea087c08f-20160118; qk_app_id=15'
    home_index(cookie)
    # login('6A5261DE-BDB3-11E5-9DB6-A45E60C0FD7B','95E77745-BDB3-11E5-A4E5-A45E60C0FD7B','32839361')
    # print('main')
    # get_uuid('EF6CA97F-8BDE-4831-B8A3-4843273F924E')
    alipay_withdraw(cookie, 50)

    home_index(cookie)
