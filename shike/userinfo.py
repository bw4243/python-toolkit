#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib
import json
from moneydb.models import User
from myutils import *
from moneydb import db
import taskrunner
from moneydb.constants import *


def get_header(cookie):
    return headers_from_str('''
        Accept:application/json, text/javascript, */*; q=0.01
        Accept-Language:zh-CN,zh;q=0.8,en;q=0.6
        Connection:keep-alive
        Content-Type:application/x-www-form-urlencoded; charset=UTF-8
        Cookie:%s
        Host:i.appshike.com
        Origin:http://i.appshike.com
        User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1
        X-Requested-With:XMLHttpRequest
    ''' % cookie)


def get_user_finance(user):
    """
    查询用户财务信息
    :param user:
    :return:
    """

    url = 'http://i.appshike.com/itry/income/getUserFinance'
    content = 'openidMD5=%s&cur_time=%d' % (user.oid_md5, datetime.datetime.now().microsecond)

    resp = http_retry(url, method='POST', body=content, headers=get_header(user.cookie))

    obj = json.loads(resp)
    # print(response.read())
    # print('今日收入:%s' % obj['today_income'].encode('UTF-8'))

    for k, v in obj.items():
        if v and u'元' in v:
            obj[k] = float(v.encode('UTF-8')[:-3])

    return obj


def has_money_up(user):
    """
    余额是否增长了
    :return: True/False
    """
    finance = get_user_finance(user)
    if finance['history_income'] > user.total_income:
        # 钱加上去了
        user.total_income = finance['history_income']
        return True
    return False


def sync_user_info(user):
    """
    同步用户基本信息 ,如 余额,收入等
    :param user:
    :return:
    """
    finance = get_user_finance(user)
    s = db.session()
    s.query(User).filter(User.id == user.id).update({
        User.balance: finance['can_withdrawal'],
        User.total_income: finance['history_income'],
        User.today_income: finance['today_income'],
        User.freeze_status: finance['user_status'] != '0'
    })
    s.commit()
    s.close()


def bind_info(user):
    log_download_xb(user)

    ss = 'bs=%s&cc=110' % user.field1

    abc = 'user_id=%s&oid_md5=%s&binding=18_1&idfa=%s&idfv=%s&uid=%s&sn=no&%s&dm=iPhone8,2&sv=8.1.2&ot=-' + random_number_str(
        5) + '&mac=&rm=c2:42:d2:26:' + random_str(2) + ':' + random_str(2) + '&ri=' + random_number_str(
        2) + '.24.' + random_number_str(3) + '.100&dt=(null)&ut=451&ls=' + random_number_str(
        11) + '&pn=18&ver=1.19&rn=' + random_str(4)
    content = abc % (user.user_id, user.oid_md5, user.idfa, user.idfv, user.uid, ss)
    taskrunner.json_time(str(content), url='http://xb.appshike.com/json')

    # content = 'user_id=%s&idfa=&bs=F5D545302WJG5NYA3&cc=340&app=1611445442,333206289,com.alipay.iphoneclient,474278250,0,143465,1,9.5.1%s1611445442,425349261,com.netease.news,474534964,0,143465,1,474%s(null),0,com.sogou.sogouinput,454115166,0,0,1,3.0.0' \
    #           % (user.user_id,  '%7C%7C', '%7C%7C')
    content = 'user_id=' + user.user_id + '&idfa=&' + ss + '&app=1611445442,333206289,com.alipay.iphoneclient,474278250,0,143465,1,9.5.1%7C%7C1611445442,425349261,com.netease.news,474534964,0,143465,1,474%7C%7C(null),0,com.sogou.sogouinput,454115166,0,0,1,3.0.0%7C%7C(null),0,com.dianping.mp.mobile,471349340,0,0,1,4.1.0%7C%7C(null),0,com.google.chrome.ios,455139072,0,0,1,43.2357.51%7C%7C10037034958,351091731,com.dianping.dpscope,475571285,1,143465,1,8.0.0%7C%7C847712612,444934666,com.tencent.mqq,455195462,0,143465,1,5.6%7C%7C(null),0,com.dianping.apollo.crm,464783782,0,0,1,2.0.0.2%7C%7C(null),0,com.tongbu.tui.9675F56748,454500304,0,0,1,3.3.2%7C%7C(null),0,com.vstudio.PeakCamera,449226728,0,0,1,0.9.99%7C%7C1611445442,921478733,com.didapinche.taxi,475570075,0,143465,1,3.4.0%7C%7C' + user.user_id + '&ver=1.19&type=d_package'
    taskrunner.json_time(str(content), replace=1)

    content = 'user_id=' + user.user_id + '&idfa=&' + ss + '&app=847712612,350962117,com.sina.weibo,453928544,0,143465,1,5.3.0%7C%7C10037034958,547166701,com.baidu.netdisk,475503388,0,143465,1,6.9.4%7C%7C(null),0,com.gad.shiliu,475550728,0,0,1,1.19%7C%7C1611445442,878534496,com.penglzh.Super12306,472454167,0,143465,1,2.0%7C%7C(null),0,com.tencent.eim,464636026,0,0,1,74557%7C%7C10037034958,414478124,com.tencent.xin,473205693,0,143465,1,6.3.9%7C%7C847712612,414245413,com.360buy.jdmobile,455462496,0,143465,1,22026%7C%7C' + user.user_id + '&ver=1.19&type=d_package'
    taskrunner.json_time(str(content), replace=1)

    content = 'user_id=%s&%s&idfa=%s&idfv=%s&uid=%s&mac=c2:41:d4:26:bc:6f&usb=28.000000&app=launchd,112685.932940,16390||nfcd,112673.934593,16388||WeChat,98017.934869,16388||eapolclient,167.936738,16644||com.apple.WebKit,62.936910,16388||com.apple.WebKit,62.936985,16388||com.apple.WebKit,61.937043,16388||com.apple.WebKit,40.937272,16388||shiliu,8.937662,16388||com.apple.WebKit,0.937784,16388||&ver=1.19&type=d_process' \
              % (user.user_id, ss, user.idfa, user.idfv, user.uid)
    taskrunner.json_time(str(content))


def add_user(user_id, nick_name, cookie, oid_md5):
    user = User(
        user_id=user_id,
        nick_name=nick_name,
        cookie=cookie,
        oid_md5=oid_md5,
        app_type=APP_TYPE_XIAO_BIN,
        idfa=gen_uuid(),
        idfv=gen_uuid(),
        uid=random_str(40),
        today_income=1,
        total_income=1,
        field1='F5' + random_str(15).upper(),
        field2=random_number_str(9)
    )

    db.add(user)

    user = User.get(user_id)
    # 绑定硬件信息
    bind_info(user)


def log_download_xb(user):
    # 小妮子 {"rtn":1,"binding":"17_1"}
    logger.info(http_retry('http://i.appshike.com/itry/log_download_xb?oid_md5=%s' % user.oid_md5,
                           headers=get_header(user.cookie)))


def chongliuliang(user):
    '''
    0: {sellingPrice: "3", shopProductName: "联通全国20M", shopProductId: "000000004d9f2a6d014db6e97a2300cf"}
    1: {sellingPrice: "6", shopProductName: "联通全国50M", shopProductId: "000000004cdff715014ce05ff5d70000"}
    2: {sellingPrice: "9.5", shopProductName: "联通全国100M", shopProductId: "000000004d9f2a6d014db6ea579400ef"}
    3: {sellingPrice: "14", shopProductName: "联通全国200M", shopProductId: "000000004d375387014d41da22a8002f"}
    4: {sellingPrice: "28", shopProductName: "联通全国500M", shopProductId: "000000004d9f2a6d014db6ec9e29010f"}
    '''

    liuliangset = {

    }
    content = 'product=%s&czPhone=18521058664&oidMd5=%s&catName=%s&option=0' % (
    '000000004d9f2a6d014db6ea579400ef', user.oid_md5, '%25E4%25B8%25AD%25E5%259B%25BD%25E8%2581%2594%25E9%2580%259A')
    resp = http_retry('http://i.appshike.com/itry/liuliangchongzhi/getLiuliangCz', method='POST',
                      headers={'cookie': user.cookie,
                               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, body=content)

    print(resp)


if __name__ == '__main__':
    add_user(user_id='19707918', nick_name=u'东山',
             cookie='OD=OYmqb9U7qHBJTG0RtdGonAhO7+4VuTZsqqBuXUWyBR5CYxK8eCmh6NDttsk3ro0l',
             oid_md5='49F2E4120DF04021A01FD07DD920A42B')
    # user = User.get('19374606')
    # bind_info(user)

    # chongliuliang(User.get('19395206'))
