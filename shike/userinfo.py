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
    试玩记录是否有该任务
    :return: True/False
    """
    content = 'start=0&length=1&is_stop=false&wechatMD5=%s&cur_time=%d' % (user.oid_md5, now_millisec())
    resp = http_retry('http://i.appshike.com/itry/personalcenter/getDailyClickRecordList', method='POST',
                      headers=get_header(user.cookie), body=content)

    print(resp)

    app_name = json.loads(resp)['list'][0].values()[0][0]['app_name']
    print(app_name)



    # finance = get_user_finance(user)
    # if finance['history_income'] > user.total_income:
    #     # 钱加上去了
    #     user.total_income = finance['history_income']
    #     return True
    # return False


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
        User.today_income: 0 if not finance['today_income'] else finance['today_income'],
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
        '000000004cdff715014ce05ff5d70000', user.oid_md5,
        '%25E4%25B8%25AD%25E5%259B%25BD%25E8%2581%2594%25E9%2580%259A')
    resp = http_retry('http://i.appshike.com/itry/liuliangchongzhi/getLiuliangCz', method='POST',
                      headers={'cookie': user.cookie,
                               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, body=content)

    print(resp)


def send_msg(user, mobile):
    '''
    给手机发验证码短信
    :param user:
    :param mobile:
    :return:
    '''
    content = 'tel=%s&openidMD5=%s&cur_time=%d' % (mobile, user.oid_md5, now_millisec())
    resp = http_retry('http://i.appshike.com/itry/personalcenter/bindingTelSendMsg', method='POST',
                      headers=get_header(user.cookie), body=content)
    print(resp)


def bind_alipay(user, mobile, code):
    '''
    绑定支付吧账户
    :param user:
    :param mobile:
    :param code:
    :return:
    '''
    content = 'bank_username=%s&vCode=%s&tel=%s&bank_num=%s&bank_flag=0&flag=%s&openidMD5=%s' % (
        '%E5%91%A8%E5%BF%97%E9%B9%8F', code, mobile, 'admin%40zhouzhipeng.com', '%E6%94%AF%E4%BB%98%E5%AE%9D',
        user.oid_md5)
    resp = http_retry('http://i.appshike.com/itry/personalcenter/bindingBankNum', method='POST',
                      headers=get_header(user.cookie), body=content)
    print(resp)


def quick_bind_user(cookie, url):
    '''
    正熙		日盈堂堂主
    易涟		月青堂堂主
    左丘宁		星鸣堂徐州御灵手
    北宫杵		星鸣堂徐州御灵手
    图尉		星鸣堂豫州御灵手
    苗巧		星鸣堂豫州御灵手
    岚宽		星鸣堂青州御灵手
    芊筱		星鸣堂青州御灵手
    单雨童		御灵团御灵手
    明降		星鸣堂勘察手
    元翔		星鸣堂勘察手
    甲子直		虎啸堂堂主，景门三煞之一，甲轩的养父
    甲兰		甲子直之女，虎啸堂大小姐
    金同福		同福镖局总镖头，景门三煞之一
    金大龙		金同福之子
    七姨太		金同福的第七个老婆，年轻貌美
    丁洪		龙吟庄庄主，景门三煞之一
    丁砂颖		龙吟庄庄主丁洪之女，丁砂平的姐姐
    丁砂平		龙吟庄庄主丁洪之子，丁砂颖的弟弟
    余万雄		万雄帮帮主
    伏龙		江湖游侠，“游龙戏凤”之一
    凤笑		江湖游侠，“游龙戏凤”之一
    郎里香		浪里花的姐姐
    仇人九		野猪坨土匪的匪首，被一个拥有十七年灵愿的灵主附体
    燕清风		甲轩生父
    燕凌霞		甲轩的姐姐

    :return:
    '''

    # cookie='OD	mjiii1eQxi7/Lldox9s+VzXs1Ymt3W+wpyhRT3OMz9Wo5SXkPQt5GLQ9nKWlTAcW	i.appshike.com	/	2017年2月21日 GMT+817:12:29	66 B	✓	'
    # cookie='OD	QgPRJzjyHbt7p1DhV8bqt3lDdJTymFt0ABqZ0PNx5YAk1iaKyvCDZzDHcFuORUcO	i.appshike.com	/	2017年2月22日 GMT+809:44:20	66 B	✓	'
    # url='/shike/getApplist/19854020/4DACC2DC425783D08009AD1A8C802F09'
    # url='/shike/getApplist/19885298/B0D611859698CA0FCE4A6AF019319B8D'
    nick_name = u'default'
    od = cookie.split('\t')[1]
    arr = url.split('/')

    userid = arr[3]
    oid = arr[4]

    print(userid)
    print(oid)
    print(od)

    add_user(user_id=userid, nick_name=nick_name,
             cookie='OD=%s' % od,
             oid_md5=oid)


def alipay_withdraw(user):
    balance = user.balance
    amount = 10
    if balance >= 100:
        amount = 100
    elif balance >= 50:
        amount = 50
    elif balance >= 30:
        amount = 30
    elif balance >= 10:
        amount = 10
    content = 'flag=no_pass&pw=&bank=%s&money=%d&openid_md5=%s&total_income=%f&cur_time=%d' % (
        user.field3, amount, user.oid_md5, user.total_income, now_millisec())
    print(content)
    resp = http_retry('http://i.appshike.com/itry/income/withdraw_deposit', method='POST',
                      headers=get_header(user.cookie), body=content)
    print(resp)
    return resp


def withdraw_record(user):
    content = 'openidMD5=%s&cur_time=%d' % (user.oid_md5, now_millisec())
    resp = http_retry('http://i.appshike.com/itry/personalcenter/getWithdrawRecordList', method='POST',
                      headers=get_header(user.cookie), body=content)
    print(resp)
    return resp


def show_alipay(user):
    content='wechatMD5=%s&cur_time=%d' % (user.oid_md5,now_millisec())
    resp=http_retry('http://i.appshike.com/itry/personalcenter/showAlipay', method='POST',
               headers=get_header(user.cookie), body=content)

    print(resp)

    obj=json.loads(resp)
    if obj['success'] and obj.has_key('alipayList'):
        return obj['alipayList'][0]
    else:
        return None


if __name__ == '__main__':
    # add_user(user_id='19990285', nick_name=u'桃花',
    #          cookie='OD=1YwkGJraimLZLZh6BNIG+H/5FJZ8YMhifp/hK/8iwBe7ncwODuTM9FjH/gaP7CJ2',
    #          oid_md5='ED0519339A219EC6418F3117EEE0CE38')
    # user = User.get('19374606')
    # bind_info(user)

    # chongliuliang(User.get('19707918'))

    # quick_bind_user()

    print(show_alipay(User.get('19852541')))
