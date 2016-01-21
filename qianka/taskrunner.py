#!/usr/bin/python
# -*-coding:utf-8-*-
import json
import time
from myutils import *
from db import disciple
import userinfo


# 构建参数
def params(data):
    obj = json.loads(data['now_task'])
    adid = obj['id']
    adname = obj['title']
    userid = data['userid']
    dict = {
        'adid': adid,
        'adname': adname,
        'check_click': '0',
        'deviceid': data['idfa'],
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


def __get_header(cookie):
    return {
        'Cookie': cookie,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": 'zh-cn',
        "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
        "Connection": 'keep-alive',
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
    }


def setting(idfa, uuid):
    print(http_retry(
        'http://api.guo7.com/setting.php?app=qk_key_1_16-13&bundleid=com.sws.app&channel=3&idfa=%s&uuid=%s&version=2.0' % (
            idfa, uuid)))


# 抓取任务
def fetch_task(data):
    headers = __get_header(data['cookie'])
    resp = http_retry('http://m.qianka.com/api/h5/subtask/fetch', headers=headers)

    # if type(resp)==type('a'):
    resp = resp.decode('unicode-escape')
    # print(resp)
    tasklist = json.loads(resp).get('data', [])

    availableTasks = []
    for task in tasklist:
        # 筛选进行中的任务
        if task['type'] == 1 and task['qty'] > 0 and task['status_order'] == 2 and task['status'] == 1:
            availableTasks.append(task)

    print("availableTasks: %s" % availableTasks)

    # 排序
    # if len(availableTasks) > 1:
    #     availableTasks.sort(key=lambda x: int(x['qty']))

    return availableTasks


# 抢任务
def start_v2(task, data):
    # 1. 抢任务
    resp = http_retry('http://m.qianka.com/api/h5/subtask/start_v2', method='POST',
                      headers=__get_header(data['cookie']),
                      body='{"task_id":%d}' % task['id'])

    resp = resp.decode('unicode-escape')
    print("start_v2 resp:%s" % resp)
    return json.loads(resp)['data']['type']


# 上传app下载状态
def upload_app_status(data):
    url = 'http://gaos.guo7.com/zq_api/index.php/lianmeng/ziji?%s' % params(data)
    _headers = {
        'Accept': '*/*',
        'User-Agent': 'QiankaKey/2.0 (iPhone; iOS 8.3; Scale/2.00)',
        'Accept-Language': 'zh-Hans;q=1',
        # 'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'

    }

    resp = http_retry(url, headers=_headers)
    if json.loads(resp)['success'] == 'true':
        # 徒弟贡献值+1
        data['contrib'] += 1
        disciple.inc_contrib(data['userid'])
    else:
        i = 0
        while json.loads(resp)['success'] == 'false' and i < 2:
            i += 1
            resp = http_retry(url, headers=_headers)
            print("uploadAppStatus resp:%s" % resp.decode('unicode-escape'))
            time.sleep(2)

    print("uploadAppStatus resp:%s" % resp.decode('unicode-escape'))


def task_detail(cookie, task_id):
    print(http_retry('http://m.qianka.com/api/h5/subtask/get?task_id=%s' % task_id, headers=headers_from_str("""
        Host: m.qianka.com
        Accept: application/json, text/plain, */*
        Connection: keep-alive
        Cookie: %s
        User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4
        Accept-Language: zh-cn
    """ % (cookie))))


# 执行任务
def complete_task(data):
    tasklist = fetch_task(data)
    for task in tasklist:

        if data['contrib'] >= 3: break

        s1 = start_v2(task, data)
        s2 = start_v2(task, data)
        #
        # if s1 == 2 or s2 == 2:
        # succeed
        print("start_v2 ok")

        # setting(data['idfa'], data['uuid'])
        # getoneself_info
        task_id = str(task['id'])

        info = userinfo.getoneself_info(task_id, data)

        # # 放入数据库,让job去上传app状态
        data['has_uncompleted'] = 1
        data['start_time'] = int(time.time())
        data['wait_seconds'] = int(info['submiao'])
        data['now_task'] = json.dumps({'id': task_id, 'title': task['title']})
        disciple.update_task_info(data)
        #
        break


        # 上传app下载状态
        # upload_app_status( data)


if __name__ == '__main__':
    while 1:
        # 1. 抓取120个徒弟,开始做任务啦
        for data in disciple.fetch_valid(100):
            complete_task(data)

        time.sleep(1)

        # test

        # while 1:
        #     complete_task({
        #                   'cookie': 'aliyungf_tc=AQAAABnMrwx1RgQABoSZtF8IrlKTFD2Y; gaoshou_session=eyJpdiI6Imd6VzczZ0FQVzhXdVZzQkpYZ2orYWc9PSIsInZhbHVlIjoiRk8xRTZ0MDYyVnlybElQNVhhbzJ6NjdJbjFsUU5LK3hzMVJtVHJkTmt2TElTdU5WOFdsMFwvV1RjdEE5bUlWNEFpSE54Q2hZUlk3bE13QVZvMXowQXdnPT0iLCJtYWMiOiIzNzc5ODJmZGM2NGQwMjdjMDhhNWQzNmY2MzA2YzIwZDE0MTIzMzc5M2E0YmE1MTYxMTE4OGM1MGMyYzE5NmI5In0%3D; PHPSESSID=a7ae13340da937d4931e583e9409abc0f5021f47; qk_app_id=13; qk_ll=eyJpdiI6IjdlOU1qRWErVktHZExcL0xRdlhkY293PT0iLCJ2YWx1ZSI6InltemxIN1NuK0FZOE5RZ29Qdm4xWWc9PSIsIm1hYyI6ImZjZmQ0YzY0MmFlOGIzNTI5NDQzNjFhMDRkMmUyNmI5NTFiMzg5NWZmNTk0YTBhOGYwODY0Zjg5ZTBiZmJiYjAifQ%3D%3D; qk:guid=bd86a9c0-b3c0-11e5-8b24-cdc5e0ec6fea-20160105',
        #                   'idfa': '5268855F-AA59-4BFE-B64F-61D04F19DE3C',
        #                   'uuid': '15CECF34-57F1-41A9-9740-477DA0A7C95B',
        #                   'userid': '32483806',
        #                   'contrib':0})
        #     time.sleep(1)
