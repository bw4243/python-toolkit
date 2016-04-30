#!/usr/bin/python
# -*-coding:utf-8-*-

"""
点评小工具集
"""

import httplib
import time
import json
import urllib
from myutils import *


def print_cityids():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    list = json.loads(http_retry('http://meta.open.dp/metadata/city/all'))
    map = {}
    for city in list:
        map[city['cityName']] = city['cityID']
    cityids = ''
    for cityname in u'鞍山 保定 北京 常州 成都 大连 东莞 佛山 福州 抚顺 广州 贵阳 哈尔滨 杭州 合肥 呼和浩特 惠州 济南 嘉兴 昆明 昆山 兰州 临沂 洛阳 南昌 南京 南宁 南通 宁波 青岛 泉州 厦门 上海 绍兴 深圳 沈阳 石家庄 苏州 台州 太原 泰州 唐山 天津 潍坊 温州 无锡 武汉 西安 襄阳 徐州 烟台 扬州 宜昌 义乌 银川 长春 长沙 镇江 郑州 中山 重庆 珠海 淄博'.split(
            ' '):
        cityids += str(map[cityname]) + ','
    #
    print(cityids)


def send_push(dpid, link, text):
    """
    发push
    :param dpid:
    :param link:
    :param text:
    :return:
    """
    # beauty-campaign-service
    content = 'url=campaign.service.couponCommonService&method=sendAppPush&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s' % (
        dpid, link, text)
    print(http_retry('http://10.1.105.166:4080/invoke.json?' + content))


def get_dpid_from_userid(userid):
    """
    从userid查询dpid
    :param userid:
    :return:
    """
    # data-server
    # content = 'url=http://service.dianping.com/dpdata/dpredis&method=get&parameterTypes=java.lang.String&parameters=bi.dprpt_userid_dpid_map.dim&parameterTypes=java.lang.String&parameters=%s' % str(userid)
    # resp=http_retry('http://10.1.106.205:4080/invoke.json?' + content)

    content = 'url=http://service.dianping.com/dpdata/dpuser&method=getUserDpidByUserid&parameterTypes=int&parameters=%s' % (
        userid)
    resp = http_retry('http://10.1.111.112:4080/invoke.json?' + content)
    print(resp)
    return resp


def test():
    ss = u"""
    获得了大众点评丽人88元礼包！
    获得了西十区1000元礼包！
    获得了小红书66元礼包！
    获得了唯品会188元礼包！
    获得了大众点评电影5元礼包！
    获得了大众点评酒店30元礼包！
    获得了西堤厚牛排30元礼包！
    获得了价值599元Dior香水！
    获得了马上诺30元礼包！
    """
    arr = ss.split('\n')
    print(arr)
    name = [u'大', 'B', u'感', u'西', u'萌', u'小', u'啦', u'萝', u'绿', u'咻', u'云', u'想', u'么', 'A', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J', 'L', 'M', 'N', 'O']
    for i in range(200):
        print(name[random.randint(0, len(name) - 1)] + '**' + name[random.randint(0, len(name) - 1)] + arr[
            random.randint(1, len(arr) - 2)])


def youhuicuxiao(accountId, contractID, beginTime, endTime, productId, shopId, itemId):
    """
    优惠促销补数据
    :return:
    """

    privilegeDto = {'orderSource': 0, 'accountId': accountId, 'extOrderId': contractID}
    privilegeitemDto = [
        {'beginTime': beginTime, 'endTime': endTime, 'productId': productId, 'shopId': shopId, 'itemId': itemId}]

    privilegeDto['shtPrivilegeItemDtos'] = privilegeitemDto

    jsonStr = urllib.quote(json.dumps(privilegeDto))

    print(jsonStr)

    content = 'url=http://service.dianping.com/mercahntShopdiyPrivilegeService/shtBaseFunctionService_1.0.0&method=addShtPrivilege&parameterTypes=com.dianping.merchant.shopdiy.privilege.api.dto.ShtPrivilegeDto&parameters=%s' % jsonStr

    print(content)

    resp = http_retry('http://merchant-shopdiy-privilege-service02.nh:4080/invoke.json?' + content)
    print(resp)
    return resp


def set_cache(category, params, value,beta=True):
    """
    设置缓存值
    :param category:
    :param params:
    :param value:
    :return:
    """
    content = 'url=campaign.service.configService&method=setCache&parameterTypes=java.lang.String&parameters=%s&parameterTypes=[Ljava.lang.Object;&parameters=%s&parameterTypes=java.lang.Object&parameters=%s' % (
        category, str(params), value)
    print(content)
    resp = http_retry( 'http://%s:4080/invoke.json?%s' % (['beauty-campaign-service02.nh','beauty-campaign-service01.beta'][beta],content))
    print(resp)


def get_cache(category, params,beta=True):
    """
    获取缓存值
    :param category:
    :param params:
    :return:
    """
    content = 'url=campaign.service.configService&method=getCache&parameterTypes=java.lang.String&parameters=%s&parameterTypes=[Ljava.lang.Object;&parameters=%s' % (
        category, str(params))
    print(content)
    resp = http_retry('http://%s:4080/invoke.json?%s' % (['beauty-campaign-service02.nh','beauty-campaign-service01.beta'][beta],content))
    print(resp)
    return resp


def is_new_user(userid, sort_type='site', mobile='', dpid='', beta=False):
    """
    判断是否是某平台新用户
    :param userid:
    :param sort_type: site-全站,bu50-丽人
    :param mobile:
    :param dpid:
    :return:
    """

    servers = ['dpuser-service01.beta', 'dpuser-service04.nh']

    content = 'url=http://service.dianping.com/dpdata/dpuser&method=isFirstBuyUser&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s' % (
        userid, sort_type, mobile, dpid)
    print(content)
    resp = http_retry('http://%s:4080/invoke.json?%s' % (servers[beta], content))
    print(resp)
    return resp


def fix_youhui_data():
    obj = json.loads(open('/Users/zhouzhipeng/Documents/contract.txt').read())
    for item in obj['data']:
        begin, end = item['duration'].split('-')
        begin_str = datetime.datetime.strptime(begin, '%Y%m%d%H%M%S').strftime('%Y-%m-%dT%H:%M:%S.000+0800')
        end_str = datetime.datetime.strptime(end, '%Y%m%d%H%M%S').strftime('%Y-%m-%dT%H:%M:%S.000+0800')

        youhuicuxiao(accountId=item['accountId'], contractID=item['contractID'], beginTime=begin_str, endTime=end_str,
                     productId=item['productId'],
                     shopId=item['shopId'], itemId=item['itemId'])

if __name__ == '__main__':
    # send_push('-8458788633886141025', 'dianping://web?sdfsf', 'testtt2')

    # get_dpid_from_userid(183500170)

    # test()

    # youhuicuxiao(2678263,9273004,"2016-01-11T00:00:00.000+0800","2016-07-10T23:59:59.000+0800",111563,27268917,11256572)

    # youhuicuxiao(5122050, 9272877, '2016-03-21T00:00:00.000+0800', '2016-09-20T23:59:59.000+0800', 111563, 45570986,
    #              11255918);

    # youhuicuxiao(863982	,9275800,	'2016-04-08T00:00:00.000+0800','2017-04-07T23:59:59.000+0800'	,111791	,8623436,	11264594);

    # get_cache('BeautyFestivalUserGameInfo', [1])
    # set_cache('BeautyFestivalUserGameInfo',[1],'{"id":10012}')
    # get_cache('BeautyFestivalUserGameInfo', [1])

    # is_new_user('9149','c135',beta=True)


    # get_cache('BeautyBigsaleParticipant', '["global"]')

    # set_cache('BeautyBigsaleParticipant', '["global"]',120000)
    # get_cache('BeautyBigsaleParticipant', '["global"]')




    # get_cache('BeautyFestivalUserGameInfo',[859735135],beta=True)

    # set_cache('BeautyFestivalUserGameInfo',[859735135],'null')

    # get_cache('BeautyFestivalUserGameInfo',[122612660],beta=False)


    # fix_youhui_data()

    get_cache('BeautyMerchantMenu',[5316709],beta=False)

    # set_cache('BeautyMerchantMenu',[5316709],'null',beta=False)

    # get_cache('testzhou',[1],beta=False)
    pass