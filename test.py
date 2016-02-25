#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib
import time
import json
import urllib
from myutils import *

# list = json.loads(http_retry('http://meta.open.dp/metadata/city/all').encode('utf-8'))
# map = {}
# for city in list:
#     map[city['cityName']] = city['cityID']
#
# cityids = ''
# for cityname in u'南昌,上海,北京,杭州,广州,南京,苏州,深圳,成都,重庆,天津,宁波,无锡,厦门,武汉,西安,沈阳,大连,青岛,济南,石家庄,哈尔滨,合肥,郑州,长沙'.split(','):
#     cityids += str(map[cityname]) + ','
#
# print(cityids)

ret = ''
dest = 'd9b733413476464e3df747d89f5828ea'
cc = '@@@@5^:^145^:^31A21e11p01p9@8_7d6r4w3s2s1@0P'

# while ret != dest:
#     resp = http_retry('http://api.adsoin.com/api/ios/system/CIPHER.php?version=1_1&sdk_type=company&date=20160221',
#                       headers={'sign': 'c3afd99fa97215b3ab138202dccdf175'})
#     cipher = json.loads(resp)['cipher']
#     print(cipher)
ret = md5(
    '35com.renrenxing.JDB5a880faf6fb5e60890d01bd8ad417c7555e55e59eb867dc65268855F-AA59-4BFE-B64F-61D04F19DE3C1453297346%s' % (
        cc))
print(ret)
