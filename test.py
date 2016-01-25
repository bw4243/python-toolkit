#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib
import time
import json
import urllib
from myutils import *

list = json.loads(http_retry('http://meta.open.dp/metadata/city/all').encode('utf-8'))
map = {}
for city in list:
    map[city['cityName']] = city['cityID']

cityids = ''
for cityname in u'南昌,上海,北京,杭州,广州,南京,苏州,深圳,成都,重庆,天津,宁波,无锡,厦门,武汉,西安,沈阳,大连,青岛,济南,石家庄,哈尔滨,合肥,郑州,长沙'.split(','):
    cityids += str(map[cityname]) + ','

print(cityids)
