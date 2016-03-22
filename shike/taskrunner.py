#!/usr/bin/python
# -*-coding:utf-8-*-

import json
from pyDes import *
from moneydb import db
from moneydb.constants import *
from moneydb.models import Task, User
from myutils import *
import userinfo


def sort_app_list(list):
    if len(list) > 1:
        list.sort(key=lambda x: int(x['order_status_disp']))
        list = filter(lambda x: x['order_status_disp'] != '0', list)

    return list


def applist(user):
    resp = http_retry("http://i.appshike.com/shike/getApplist/%s/%s" % (user.user_id, user.oid_md5), method='POST',
                      body='r=%d' % (int(time.time() * 1000)), headers=headers_from_str('''
                        Host: i.appshike.com
                        Accept: */*
                        Accept-Language: zh-CN,zh;q=0.8,en;q=0.6
                        Connection: keep-alive
                        Content-Type: application/x-www-form-urlencoded; charset=UTF-8
                        Cookie: JSESSIONID=6DEC5C3BD071AEF96867F511FA686F2C;aliyungf_tc=AQAAAFIbwmV0ZgMABoSZtMD3aN3xR5rI;%s
                        Host: i.appshike.com
                        Origin: http://i.appshike.com
                        Referer:http://i.appshike.com/shike/appList
                        User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1
                        X-Requested-With: XMLHttpRequest
                        Cache-Control: no-cache
                        DNT: 1
                      ''' % user.cookie))
    logger.info(resp.decode('UTF-8'))

    list = json.loads(resp)

    return sort_app_list(list)


def complete_task(user):
    task_list = applist(user)
    if len(task_list) == 0:
        user.update_is_working(False)
        return

    fetched = False
    for app in task_list:
        # 可以下载
        xb_online(user)
        # print(app['search_word'])

        appid = app['appid']
        name = app['name']
        order_id = app['order_id']
        bundle_id = app['bundle_id'].encode("UTF-8")
        process_name = app['process_name'].encode("UTF-8")

        # 点击并且复制关键词
        content = "appid=%s&user_id=%s&order_Id=%s&type=app" % (appid, user.user_id, order_id)

        # 2.点击纪录
        url = 'http://i.appshike.com/shike/user_click_record'
        text = http_retry(url, method='POST', headers=userinfo.get_header(user.cookie), body=content)
        logger.info('user_click_record resp: %s' % text)

        if text != '0':
            logger.info("没抢到,库存可能不够,直接下一个")
            continue

        # 3.复制关键词
        url = 'http://i.appshike.com/shike/copy_keyword'
        text = http_retry(url, method='POST', headers=userinfo.get_header(user.cookie), body=content)
        logger.info(text)

        count=5
        while text != '0' and count>0:
            count-=1
            logger.info("have not greped ,retry!")
            text = http_retry(url, method='POST', headers=userinfo.get_header(user.cookie), body=content)
            logger.info(text)

        if text != '0':
            continue

        # 4.放入task表中,等待执行
        task = Task(
            user_id=user.user_id,
            task_id=appid,
            task_name=name,
            bundle_id=bundle_id,
            process_name=process_name,
            status=TASK_STATUS_WAIT,
            block_type=BLOCKED_TYPE_ONE,
            fire_time=after_seconds(30),
            app_type=APP_TYPE_XIAO_BIN,
            field1=order_id
        )

        print_app_status(user, task)

        fake_down_and_open(user, task)

        fetched = True

        break

    if not fetched:
        user.update_is_working(False)


def xb_online(user):
    headers = userinfo.get_header(user.cookie)
    content = 'user_id=%s&status=0' % user.user_id
    content = 'p=' + encrypt_content(content.decode('UTF-8'))
    url = 'http://xb.appshike.com/xb_online'
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
    tp = (user.user_id, user.idfa, user.field1, task.task_id, task.bundle_id, '%7C%7C', user.user_id)
    # 下载中
    content = 'user_id=%s&idfa=%s&bs=%s&cc=340&app=(null),%s,%s,473522972,0,0,0,(null)%s%s&ver=1.19&type=d_package' % tp
    json_time(content)
    print_app_status(user, task)

    # 下载完成
    tp = (user.user_id, user.idfa, user.field1, user.field2, task.task_id, task.bundle_id, '%7C%7C', user.user_id)
    content = 'user_id=%s&idfa=%s&bs=%s&cc=340&app=%s,%s,%s,473523166,0,143465,1,2.110.0%s%s&ver=1.19&type=d_package' % tp
    json_time(content)
    print_app_status(user, task)

    # task存入数据库
    db.add(task)


def upload_process_status(user, task):
    content = 'user_id=%s&bs=%s&cc=110&idfa=%s&idfv=%s&uid=%s&mac=80:89:17:87:49:91&usb=46.000000&app=launchd,2291948.993783,16390||CVMServer,606019.996496,16388||WeChat,3516.999015,16388||BDPhoneBrowser,3051.999252,16388||SafariCloudHisto,2734.999395,16388||dongxiang,2666.999904,16388||nanoregistryd,2609.000210,16388||nanoregistrylaun,2602.000325,16388||MobileNotes,1869.001144,16388||QQ,375.002563,16388||carkitd,363.002657,16388||com.apple.WebKit,324.002822,16388||com.apple.WebKit,324.002923,16388||%s,242.003093,16388||&ver=1.19&type=d_process' \
              % (user.user_id, user.field1, user.idfa, user.idfv, user.uid, task.process_name)

    json_time(content)


def print_app_status(user, task):
    logger.info(
        http_retry(
            'http://i.appshike.com/shike/getAppStatus/%s/%s/%s' % (task.bundle_id, user.user_id, task.process_name)))


def encrypt_content(content, replace=1):
    Des_Key = "0dxwLxO8"  # Key
    Des_IV = "\x01\x02\x03\x04\x05\x06\x07\x08"  # IV向量
    k = des(Des_Key, CBC, Des_IV, padmode=PAD_PKCS5)
    encryptstr = k.encrypt(str(content))
    ret = base64.b64encode(encryptstr)  # 转base64编码返回
    if replace:
        ret = ret.replace('+', '%2B')
    else:
        ret = urllib.quote_plus(ret)
    # ret = ret.replace('+', '%2B')

    logger.info(ret)
    return ret


def give_up(user, task):
    content = 'appid=%s&order_id=%s&doingStatus=r3&user_id=%s' % (task.task_id, task.field1, user.user_id)
    resp = http_retry('http://i.appshike.com/shike/giveupApp', method='POST', headers=userinfo.get_header(user.cookie),
                      body=content)
    logger.info(resp)
    return resp


#
# 以下两个函数其他app应该都来实现,并交由job调用
#
def gen_task(user):
    """
    生成任务
    :param user:
    :return:
    """
    # 修改user状态,加锁
    user.update_is_working(True)


    try:
        complete_task(user)

    except:
        user.update_is_working(False)
        logger.exception('shike gen_task error!')

def after_run(user):
    #更新用户信息
    userinfo.sync_user_info(user)

    #0.小兵在线
    xb_online(user)

    #更新支付宝绑定信息
    # if not user.field3:
    #     result=userinfo.show_alipay(user)
    #     if result:
    #         user.update({User.field3:json.dumps(result).decode('unicode-escape')})


def has_task_completed(user,task):
    """
    试玩记录是否有该任务
    :return: True/False
    """
    content='start=0&length=1&is_stop=false&wechatMD5=%s&cur_time=%d' % (user.oid_md5,now_millisec())
    resp=http_retry('http://i.appshike.com/itry/personalcenter/getDailyClickRecordList',method='POST',headers=userinfo.get_header(user.cookie),body=content)

    print(resp)

    app_name=json.loads(resp)['list'][0].values()[0][0]['app_name']
    print(app_name)

    return task.task_name == app_name



def run_task(user, task):
    """
    执行任务
    :param user:
    :param task:
    :return:
    """


    # 1.修改task状态,防止其他job访问
    task.update_task_status(TASK_STATUS_DOING)

    try:

        upload_process_status(user, task)
        print_app_status(user, task)
        # 检查是否完成,并修改task和user状态
        if has_task_completed(user,task):
            # 可以终止了
            user.update_is_working(False)
            task.update_task_status(TASK_STATUS_COMPLETED)

            # 更新余额
            userinfo.sync_user_info(user)
        else:
            # 判断是否已经超时  默认5分钟
            if (task.update_time - task.add_time).total_seconds() > 6 * 60:
                task.update_task_status(TASK_STATUS_TIMEOUT)
                # 放弃任务
                give_up(user, task)
                user.update_is_working(False)
            else:
                # 加时
                task.update_task_firetime(after_seconds(30))
                task.update_task_status(TASK_STATUS_WAIT)
    except:
        logger.exception('shike run_task error! ')
        task.update_task_status(TASK_STATUS_WAIT)


if  __name__ == '__main__':
    user=User.get('20852965')
    # print(applist(User.get('21101999')))
    # xb_online(user)
    print(applist(user))