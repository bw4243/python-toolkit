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
        'check_click': '1',
        'deviceid': data['idfa'],
        'dsid': '382080527',
        'mdt': '476093623',
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

    logger.info('sign: %s' % sign)

    # 拼装url参数
    urlparam = ''
    for k in dict.keys():
        if k == 'adname':
            dict[k] = urllib.quote_plus(dict[k].encode('utf-8'))
        urlparam += k + '=' + dict[k] + '&'

    urlparam = urlparam[:-1]

    logger.info('urlparam :%s' % urlparam)

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
    logger.info(http_retry(
        'http://api.guo7.com/setting.php?app=qk_key_1_16-13&bundleid=com.sws.app&channel=3&idfa=%s&uuid=%s&version=2.0' % (
            idfa, uuid)))


# 抓取任务
def fetch_task(data):
    headers = __get_header(data['cookie'])
    resp = http_retry('http://m.qianka.com/api/h5/subtask/fetch', headers=headers)

    resp = resp.decode('unicode-escape')
    ret = json.loads(resp)

    if ret['code'] == 401:  # 权限异常
        data['cookie'] = userinfo.login(data['idfa'], data['uuid'], data['userid'])
        disciple.update_cookie(data)
        headers = __get_header(data['cookie'])
        resp = http_retry('http://m.qianka.com/api/h5/subtask/fetch', headers=headers)
        resp = resp.decode('unicode-escape')
        ret = json.loads(resp)

    tasklist = ret.get('data', [])

    availableTasks = []
    for task in tasklist:
        # 筛选进行中的任务
        if task['type'] == 1 and task['qty'] > 0 and task['status_order'] == 2 and task['status'] == 1:
            availableTasks.append(task)

    logger.info("availableTasks: %s" % availableTasks)

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
    logger.info("start_v2 resp:%s" % resp)
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
            url = 'http://gaos.guo7.com/zq_api/index.php/lianmeng/ziji?%s' % params(data)
            resp = http_retry(url, headers=_headers)
            logger.info("uploadAppStatus resp:%s" % resp.decode('unicode-escape'))
            time.sleep(2)

    logger.info("uploadAppStatus resp:%s" % resp.decode('unicode-escape'))


def task_detail(cookie, task_id):
    logger.info(http_retry('http://m.qianka.com/api/h5/subtask/get?task_id=%s' % task_id, headers=headers_from_str("""
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
        # if data['contrib'] >= 3: break

        s1 = start_v2(task, data)
        s2 = start_v2(task, data)
        #
        if s1 == 2 or s2 == 2:
            # succeed
            logger.info("start_v2 ok")

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


# if __name__ == '__main__':
def run(max_count):
    try:
        # 1. 抓取120个徒弟,开始做任务啦
        for data in disciple.fetch_valid(max_count):
            complete_task(data)

        # 2. 检查是否有可提交的任务
        logger.info("----check ------")
        for data in disciple.fetch_will_complete():
            upload_app_status(data)
            data['has_uncompleted'] = 0
            data['now_task'] = data['now_task'].encode('unicode-escape')
            disciple.update_task_info(data)

            # userinfo.sync_one_status(data)
    except:
        logger.exception("taskrunner exception")


if __name__ == '__main__':
    # fetch_task(disciple.fetch_masters()[0])

    upload_app_status()