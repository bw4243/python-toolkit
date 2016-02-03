#!/usr/bin/python
# -*-coding:utf-8-*-

import json
from pyDes import *
from moneydb import db
from moneydb.constants import *
from moneydb.models import Task
from myutils import *


def get_header(cookie):
    return {
        'Cookie': cookie,
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": 'zh-cn',
        "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
        "Connection": 'keep-alive',
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
    }


def sort_app_list(list):
    if len(list) > 1:
        list.sort(key=lambda x: int(x['order_status_disp']))

    return list


def applist(user):
    resp = http_retry("http://i.appshike.com/shike/getApplist/%s/%s" % (user.user_id, user.oid_md5))
    logger.info(resp)

    list = json.loads(resp)

    return sort_app_list(list)


def complete_task(user):
    for app in applist(user):
        if app['order_status_disp'] != '0':
            # 可以下载
            xb_online(user)
            # print(app['search_word'])

            appid = app['appid']
            order_id = app['order_id']
            bundle_id = app['bundle_id'].encode("UTF-8")
            process_name = app['process_name'].encode("UTF-8")

            # 点击并且复制关键词
            content = "appid=%s&user_id=%s&order_Id=%s&type=app" % (appid, user.userid, order_id)

            # 2.点击纪录
            url = 'http://i.appshike.com/shike/user_click_record'
            text = http_retry(url, method='POST', headers=get_header(user.cookie), body=content)
            logger.info(text)

            if text != '0':
                logger.info("没抢到,库存可能不够,直接下一个")
                continue

            # 3.复制关键词
            url = 'http://i.appshike.com/shike/copy_keyword'
            text = http_retry(url, method='POST', headers=get_header(user.cookie), body=content)
            logger.info(text)

            while text != '0':
                logger.info("have not greped ,retry!")
                text = http_retry(url, method='POST', headers=get_header(user.cookie), body=content)

            # 4.放入task表中,等待执行
            task = Task(
                user_id=user.user_id,
                task_id=appid,
                bundle_id=bundle_id,
                process_name=process_name,
                status=TASK_STATUS_WAIT,
                block_type=BLOCKED_TYPE_ONE,
                fire_time=after_seconds(30)
            )

            print_app_status(user, task)

            fake_down_and_open(user, task)

            # break


def xb_online(user):
    headers = get_header(user.cookie)
    content = 'user_id=%s&status=0' % user.user_id
    content = 'p=' + encrypt_content(content)
    url = 'http://xb.i.appshike.com/xb_online'
    resp = http_retry(url, method='POST', body=content, headers=headers)
    logger.info(resp)


def json_time(content, url=None, replace=0):
    content = 'p=' + encrypt_content(content, replace)
    if not url:
        url = 'http://xb.appshike.com/json_time'

    text = http_retry(url, method='POST', body=content, headers=headers_from_str("""
        Content-Type: application/x-www-form-urlencoded
        Connection: keep-alive
        Accept: */*
        User-Agent: com.gad.shiliu/1.19 CFNetwork/711.1.16 Darwin/14.0.0
        Accept-Language: zh-cn
    """))
    logger.info(text.decode('utf-8'))


def fake_down_and_open(user, task):
    tp = (user.userid, task.task_id, task.bundle_id, '%7C%7C', user.user_id)
    # 下载中
    content = 'user_id=%s&idfa=&bs=F5D545302WJG5NYA3&cc=340&app=(null),%s,%s,473522972,0,0,0,(null)%s%s&ver=1.19&type=d_package' % tp
    json_time(content)
    print_app_status(user, task)

    # 下载完成
    content = 'user_id=%s&idfa=&bs=F5D545302WJG5NYA3&cc=340&app=382080527,%s,%s,473523166,0,143465,1,2.110.0%s%s&ver=1.19&type=d_package' % tp
    json_time(content)
    print_app_status(user, task)

    # task存入数据库
    db.add(task)


def upload_process_status(user, task):
    content = 'user_id=%s&bs=F5D545302WJG5NYA3&cc=340&idfa=%s&idfv=%s&uid=%s&mac=80:89:17:87:49:92&usb=46.000000&app=launchd,2291948.993783,16390||CVMServer,606019.996496,16388||WeChat,3516.999015,16388||BDPhoneBrowser,3051.999252,16388||SafariCloudHisto,2734.999395,16388||dongxiang,2666.999904,16388||nanoregistryd,2609.000210,16388||nanoregistrylaun,2602.000325,16388||MobileNotes,1869.001144,16388||QQ,375.002563,16388||carkitd,363.002657,16388||com.apple.WebKit,324.002822,16388||com.apple.WebKit,324.002923,16388||%s,242.003093,16388||&ver=1.19&type=d_process' \
              % (user.userid, user.idfa, user.idfv, user.uuid, task.process_name)

    json_time(content)


def print_app_status(user, task):
    logger.info(
        http_retry(
            'http://i.appshike.com/shike/getAppStatus/%s/%s/%s' % (task.bundle_id, user.user_id, task.process_name)))


def encrypt_content(str, replace=1):
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

    logger.info(ret)
    return ret


def give_up(user, task):
    content = 'appid=%s&order_id=%s&doingStatus=r3&user_id=%s' % (task.task_id, task.order_id, user.user_id)
    resp = http_retry('http://i.appshike.com/shike/giveupApp', method='POST', headers=get_header(user.cookie),
                      body=content)
    logger.info(resp)
    return resp


# def run_task(user, task):


if __name__ == '__main__':
    # open('sync.txt', 'w').write('1')
    # for i in range(10):
    # 抓取有效的小兵用户


    complete_task()
