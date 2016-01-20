#!/usr/bin/python
# -*-coding:utf-8-*-
import json
import time
from myutils import *
import config

headers = {
    'Cookie': config.cookie,
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": 'zh-cn',
    "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
    "Connection": 'keep-alive',
    "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
}


# 构建参数
def params(adid, adname):
    userid = config.userid
    dict = {
        'adid': adid,
        'adname': adname,
        'check_click': '0',
        'deviceid': config.deviceid,
        'dsid': config.dsid,
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

    logger.info('sign', sign)

    # 拼装url参数
    urlparam = ''
    for k in dict.keys():
        if k == 'adname':
            dict[k] = urllib.quote_plus(dict[k].encode('utf-8'))
        urlparam += k + '=' + dict[k] + '&'

    urlparam = urlparam[:-1]

    logger.info('urlparam', urlparam)

    return urlparam


# 抓取任务
def fetchTask():
    url = 'http://m.qianka.com/api/h5/subtask/fetch'
    conn = httplib.HTTPConnection("m.qianka.com")
    conn.request(method='GET', url=url, headers=headers)
    response = conn.getresponse()
    status = response.status
    logger.info("fetch status: %d  t:%d" % (status, time.time()))

    while status != 200:
        logger.info("fetch retry")
        conn = httplib.HTTPConnection("m.qianka.com")
        conn.request(method='GET', url=url, headers=headers)
        response = conn.getresponse()
        status = response.status

    resp = response.read()
    # if type(resp)==type('a'):
    resp = resp.decode('unicode-escape')
    tasklist = json.loads(resp)['data']

    # logger.info("tasklist: %s" % str(tasklist).decode('unicode-escape'))

    availableTasks = []
    for task in tasklist:
        # 筛选进行中的任务
        if task['type'] == 1 and task['qty'] > 0 and task['status_order'] == 2 and task['status'] == 1:
            availableTasks.append(task)

    logger.info("availableTasks: %s" % availableTasks)

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
    logger.info("start_v2 status: %d" % status)

    while status != 200:
        logger.info("start_v2 retry")
        conn = httplib.HTTPConnection("m.qianka.com")
        conn.request(method='POST', url=url, headers=headers, body='{"task_id":%d}' % task['id'])
        response = conn.getresponse()
        status = response.status

    resp = response.read().decode('unicode-escape')

    try:
        logger.info("start_v2 resp:%s" % resp)
    except Exception, e:
        logger.info(e)

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
    logger.info("uploadAppStatus status: %d" % status)

    while status != 200:
        logger.info("fetch retry")
        conn = httplib.HTTPConnection("m.qianka.com")
        conn.request(method='GET', url=url, headers=_headers)
        response = conn.getresponse()
        status = response.status

    try:
        logger.info("uploadAppStatus resp:%s" % response.read().decode('unicode-escape'))
    except Exception, e:
        logger.info(e)


# 执行任务
def completeTask(tasklist):
    # if len(tasklist)>0:
    #     setting()
    #     day_journals()
    for task in tasklist:
        if (start_v2(task)['type'] == 2) or (start_v2(task)['type'] == 1 and start_v2(task)['type'] == 2):
            # succeed
            logger.info("start_v2 ok")

            # getoneself_info
            task_id = str(task['id'])
            # getoneself_info(task_id)

            # 上传app下载状态
            uploadAppStatus(task_id, task['title'])


# setting
def setting():
    logger.info(http_retry(
        "http://api.guo7.com/setting.php?app=qk_key_1_16-13&bundleid=com.sws.app&channel=3&idfa=5268855F-AA59-4BFE-B64F-61D04F19DE3C&uuid=15CECF34-57F1-41A9-9740-477DA0A7C95B&version=2.0"))


#
if __name__ == '__main__':
    try:
        for i in range(29):
            completeTask(fetchTask())
            time.sleep(2)
    except:
        logger.exception("Exception Logged")


        # getoneself_info('123477')

# day_journals()

# logger.info(params('124131','掌上电玩城'))


# fetchTask()
# setting()
# uploadAppStatus('124266',u'天天暴走')

# ss=u'\u8bbe\u5907\u7c7b\u578b\u9519\u8bef'
#
# logger.info(type(ss))
# #
# # # ss=unicode(ss,'utf-8')
# # ss=ss.decode('ascii').encode('utf-8')
# #
# ss=ss.decode('unicode-escape')
#

# ss=ss.decode('unicode-escape')
# logger.info(ss)
