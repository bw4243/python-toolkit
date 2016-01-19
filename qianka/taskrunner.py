#!/usr/bin/python
# -*-coding:utf-8-*-
import json
import time
from myutils import *
from db import disciple


# 构建参数
def params(adid, adname, data):
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


# 抓取任务
def fetch_task(data):
    headers = __get_header(data['cookie'])
    resp = http_retry('http://m.qianka.com/api/h5/subtask/fetch', headers=headers)

    # if type(resp)==type('a'):
    resp = resp.decode('unicode-escape')
    tasklist = json.loads(resp)['data']

    availableTasks = []
    for task in tasklist:
        # 筛选进行中的任务
        if task['type'] == 1 and task['qty'] > 0 and task['status_order'] == 2 and task['status'] == 1:
            availableTasks.append(task)

    print("availableTasks: %s" % availableTasks)

    # 排序
    if len(availableTasks) > 1:
        availableTasks.sort(key=lambda x: int(x['qty']))

    return availableTasks


# 抢任务
def start_v2(task, data):
    # 1. 抢任务
    resp = http_retry('http://m.qianka.com/api/h5/subtask/start_v2', method='POST',
                      headers=__get_header(data['cookie']),
                      body='{"task_id":%d}' % task['id'])

    resp = resp.decode('unicode-escape')
    print("start_v2 resp:%s" % resp)
    return json.loads(resp)['data']


# 上传app下载状态
def upload_app_status(adid, adname, data):
    url = 'http://gaos.guo7.com/zq_api/index.php/lianmeng/ziji?%s' % params(adid, adname, data)
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

    print("uploadAppStatus resp:%s" % resp.decode('unicode-escape'))


# 执行任务
def complete_task(data):
    tasklist = fetch_task(data)
    for task in tasklist:

        if data['contrib'] >= 10: break

        start_v2(task, data)
        start_v2(task, data)
        # succeed
        print("start_v2 ok")

        # getoneself_info
        task_id = str(task['id'])
        # getoneself_info(task_id)

        # 上传app下载状态
        upload_app_status(task_id, task['title'], data)


if __name__ == '__main__':
    while 1:
        # 1. 抓取120个徒弟,开始做任务啦
        for data in disciple.fetch_valid(120):
            if data['contrib'] < 10:
                complete_task(data)

        time.sleep(2)