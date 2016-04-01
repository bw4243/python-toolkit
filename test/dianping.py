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
    # beauty-campaign-service
    content = 'url=campaign.service.couponCommonService&method=sendAppPush&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s' % (
        dpid, link, text)
    print(http_retry('http://10.1.105.166:4080/invoke.json?' + content))


def get_dpid_from_userid(userid):
    # data-server
    content = 'url=http://service.dianping.com/dpdata/dpredis&method=get&parameterTypes=java.lang.String&parameters=bi.dprpt_userid_dpid_map.dim&parameterTypes=java.lang.String&parameters=%s' % str(userid)
    resp=http_retry('http://10.1.106.205:4080/invoke.json?' + content)
    print(resp)
    return resp

if __name__ == '__main__':
    # send_push('-8458788633886141025', 'dianping://web?sdfsf', 'testtt2')

    get_dpid_from_userid(183500170)