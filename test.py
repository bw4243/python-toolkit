#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib
import time
import json
import urllib
from myutils import *

reload(sys)
sys.setdefaultencoding("utf-8")

list = json.loads(http_retry('http://meta.open.dp/metadata/city/all'))
map = {}
for city in list:
    map[city['cityName']] = city['cityID']

cityids = ''
for cityname in u'北京、福州、广州、杭州、合肥、宁波、青岛、厦门、上海、深圳、沈阳、苏州、天津、武汉、长沙、郑州、西安、重庆、成都'.split('、'):
    cityids += str(map[cityname]) + ','

print(cityids)
#
# ret = ''
# dest = 'd9b733413476464e3df747d89f5828ea'
# cc = '@@@@5^:^145^:^31A21e11p01p9@8_7d6r4w3s2s1@0P'
#
# # while ret != dest:
# #     resp = http_retry('http://api.adsoin.com/api/ios/system/CIPHER.php?version=1_1&sdk_type=company&date=20160221',
# #                       headers={'sign': 'c3afd99fa97215b3ab138202dccdf175'})
# #     cipher = json.loads(resp)['cipher']
# #     print(cipher)
# ret = md5(
#     '35com.renrenxing.JDB5a880faf6fb5e60890d01bd8ad417c7555e55e59eb867dc65268855F-AA59-4BFE-B64F-61D04F19DE3C1453297346%s' % (
#         cc))
# print(ret)
