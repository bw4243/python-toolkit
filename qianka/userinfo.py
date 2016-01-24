#!/usr/bin/python
# -*-coding:utf-8-*-
import time
from myutils import *
import json
from db import disciple

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def bind_master(cookie, master_id):
    print(http_retry('http://m.qianka.com/api/h5/gift/first', headers={
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'}, method='POST', body='{"master_id":%s}' % master_id))


def home_index(cookie):
    resp=http_retry('http://m.qianka.com/api/h5/home/index', headers=headers_from_str("""
        Host: m.qianka.com
        Accept: application/json, text/plain, */*
        Connection: keep-alive
        Cookie: %s
        User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4
        Accept-Language: zh-cn
        Referer: http://m.qianka.com/fe/dashboard/index.html?timestamp=1453093214978
    """ % cookie)).decode('unicode-escape')
    print(resp)
    return json.loads(resp)['data']




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


def getoneself_info(task_id, data):
    content = params2("""
                batteryCapacityLeft	46
                bssid	cc:46:d6:26:bc:6f
                bundleid	com.sws.app
                deviceID	7105089584816
                freeDiskspace	2230
                idfa	%s
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
                task_id	%s
                timestamp	1452062787.439038
                totalDiskspace	12305
                uuid	%s
                version	2.0.2015122101

                """ % (data['idfa'], task_id, data['uuid']))

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

    return json.loads(resp)


# 批量生产徒弟
def batch_gen(master_id='0',count=1):
    # 绑定master
    for i in range(count):
        idfa, uuid, user_id, cookie = reg_get_user()
        if master_id != '0':
            bind_master(cookie, master_id)

        disciple.new_disciple(idfa, uuid, user_id, cookie, master_id)

        time.sleep(2)
        print("===================>>>>>>>>>>")


# print(disciple.fetch_valid())


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


def weixin_withdraw(cookie,realname, amount):
    print(http_retry('http://m.qianka.com/api/h5/exchange/dowxpay', method='POST', headers=headers_from_str("""
        Accept: application/json, text/plain, */*
        Accept-Language: zh-cn
        Content-Type: application/json;charset=UTF-8
        Origin: http://m.qianka.com
        Connection: keep-alive
        User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4
        Cookie: %s
    """ % cookie), body='{"realname":"%s","price":%d}' % (realname,amount)).decode('unicode-escape'))


def voice_code(cookie, mobile):
    print(http_retry('http://m.qianka.com/api/h5/voice/code', method='POST', headers=headers_from_str("""
        Host: m.qianka.com
        Accept: application/json, text/plain, */*
        Accept-Language: zh-cn
        Content-Type: application/json;charset=UTF-8
        Origin: http://m.qianka.com
        Connection: keep-alive
        User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4
        Cookie: %s
    """ % cookie), body='{"mobile":%s}' % mobile).decode('unicode-escape'))


def bind_mobile(cookie, mobile, code):
    print(http_retry('http://m.qianka.com/api/h5/user/bindmobile', method='POST', headers=headers_from_str("""
        Host: m.qianka.com
        Accept: application/json, text/plain, */*
        Accept-Language: zh-cn
        Content-Type: application/json;charset=UTF-8
        Origin: http://m.qianka.com
        Connection: keep-alive
        User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4
        Cookie: %s
    """ % cookie), body='{"mobile":%s,"code":"%s"}' % (mobile, code)).decode('unicode-escape'))


def freeze_status(cookie):
    resp = http_retry('http://m.qianka.com/api/h5/clientcenter/freezestatus', headers={'cookie': cookie})
    print(resp)
    return json.loads(resp)['data']['account_status']


def sync_user_status():
    for d in disciple.fetch_masters():
        data=home_index(d['cookie'])
        disciple.update_account_status(d['id'], freeze_status(d['cookie']),data['balance'],data['total_income'],data['today_income'])


def gen_disciples_for_all():
    for d in disciple.fetch_masters():
        batch_gen(master_id= d['userid'],count=2)

if __name__ == '__main__':
    # login()
    # add_user()
    # reg_get_user()
    # bind_master()
    # cookie = 'aliyungf_tc=AQAAAHSRzEQXRwEABoSZtNrgiX1imW0r; gaoshou_session=eyJpdiI6IlFKREpQUkV5WGk2QkVnanNzUldqWXc9PSIsInZhbHVlIjoiakVYK1FtMnRIUlk4SUtzTXFJY0l1Y3FaTEVvZDlUNVVuME9LS0duVlpFaFZkQTFVdEdlcG9TYlNqWE94RzVJM2xiRFhaOWJYUU9iVVlZRDhVMnJ1U0E9PSIsIm1hYyI6ImE0MjZhM2I3N2IwYTQ5ZjBhODMzMWUzMzdiY2VlYjc1Mzc3MTI2MTljNTAzMzViNzU5NTFjMTE4ZDNmNjM2MTcifQ%3D%3D; PHPSESSID=bd7a1528e45d477fac27859f17bed60de9a53c5d; qk:guid=93e8deb0-bd9f-11e5-86c8-bbbea087c08f-20160118; qk_app_id=15'
    # cookie = 'aliyungf_tc=AQAAAKCjIzFLdwsABoSZtDJalQR+PiEw;  PHPSESSID=6ea8dfb1f18eb3278498f05752dcdf09d93ef284; expires=Mon, 25-Jan-2016 13:19:19 GMT; Max-Age=604800;  gaoshou_session=eyJpdiI6IjF3aFZ2WkZCdVN4em1cLzV1SnpIbmpBPT0iLCJ2YWx1ZSI6IklhbjRsMTlYVFwvWHBlQ0dEbUZBNXRXdVVpbGRKTmZxOVhQdEdxMndvSVJ6QjRoOEdqNmZqRHR2dUlHWTViTWtDZXJGNjl5cGhsTHBPd0ZyNTdpUzhidz09IiwibWFjIjoiZGVhYWIxYmUyZDJmNmNmYzhmODQ0ZWI2NzhjZDQ2MTNjYzU1MmY5YTU0MDZjN2FjN2Q1MDFhODM5YjM2NGYyMSJ9; expires=Mon, 25-Jan-2016 13:19:19 GMT; Max-Age=604800; path=/; httponly'
    # home_index(cookie)
    # # login('6A5261DE-BDB3-11E5-9DB6-A45E60C0FD7B','95E77745-BDB3-11E5-A4E5-A45E60C0FD7B','32839361')
    # # print('main')
    # # get_uuid('EF6CA97F-8BDE-4831-B8A3-4843273F924E')
    # alipay_withdraw(cookie, 10)
    #
    # home_index(cookie)

    # voice_code(cookie,'18521058664')


    # batch_gen()

    # freeze_status(
    #     'aliyungf_tc=AQAAAFVED2h4YAAABoSZtF/r17TimfGo;  PHPSESSID=156c3f3ae2ca2e6682fa86e3d645f0c5d2828d86; expires=Mon, 25-Jan-2016 13:20:20 GMT; Max-Age=604800;  gaoshou_session=eyJpdiI6ImdoZkFFcWZyTWdhN2VBRm0xZTJOcnc9PSIsInZhbHVlIjoiOWFMWWw1M2QyTzBpdWxQa2g3MkMzZGFLU2dxcDJkMkhxRzBYSUhiMTNtdnp1ZGNvdXhOaVdqSDdXVUJIbFFaK3lHVDl0Qlk0Q1AwenJnaTVVYjVMTGc9PSIsIm1hYyI6IjJmNGM5NzI2ODA3MTliNTAxMmMxYTBkY2JmOGZmNTUwNTZkY2IwZGMwNTA1NjUxNmU4OTM1Zjk3ZWFlODkzOGYifQ%3D%3D; expires=Mon, 25-Jan-2016 13:20:20 GMT; Max-Age=604800; path=/; httponly')

    # me=disciple.fetch_masters()[0]
    # weixin_withdraw(me['cookie'],me['withdraw_realname'],10)

    sync_user_status()
    # batch_gen('33005806')

    # gen_disciples_for_all()

    # alipay_withdraw('aliyungf_tc=AQAAAF8zwWOUTgQABoSZtC+qxGVk0/CC;  PHPSESSID=e03e198e26a1e468a393268db4d73813d8126ec7; expires=Thu, 28-Jan-2016 09:04:14 GMT; Max-Age=604800;  gaoshou_session=eyJpdiI6ImdEUFdXNTdoOExYc0dmNnFFbUhcL0tRPT0iLCJ2YWx1ZSI6IkVOVVNYXC8zQllXV2tIZ2FCaGRsaThPTUtQanpab0RqM2IzUThpSGpaWHhqNmFpWHRvQ3BYNnNwblZENkhzYWlzaVBjWDBoQnBrZ2xkK1JUbWV2ejFPUT09IiwibWFjIjoiZThlYWI0MzA4ZTgyNDI2NTg2NjAzOTBlMjk2ODAwMmJlYjNhNDc1NzNlOTE1ZjdiMDE1MjBmMGU3OWZjMTU1OSJ9; expires=Thu, 28-Jan-2016 09:04:14 GMT; Max-Age=604800; path=/; httponly',10)

    # print(login('5268855F-AA59-4BFE-B64F-61D04F19DE3C','15CECF34-57F1-41A9-9740-477DA0A7C95B','32483806'))


