#!/usr/bin/python
# -*-coding:utf-8-*-
import hashlib
import httplib
import urllib
import base64
import os
import logging
import logging.handlers
import uuid
import os
import sys
import time
import datetime
import random


def after_seconds(secs):
    dt = datetime.datetime.utcfromtimestamp(time.time() + secs)
    dt = dt + datetime.timedelta(hours=8)
    return dt


def now():
    return datetime.datetime.now()


def str2time(str):
    timeArray = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳:
    return int(time.mktime(timeArray))


def time2str(timestamp):
    timeArray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def nowtime_str():
    return time2str(int(time.time()))


def gen_uuid():
    return str(uuid.uuid4()).upper()


def random_str(length):
    ss = '0123456789abcdefghijklmnopqrstuvwxyz'
    ret_str = ''
    for i in range(length):
        index = random.randint(0, len(ss) - 1)
        ret_str += ss[index]
    return ret_str


def random_number_str(length):
    ss = '0123456789'
    ret_str = ''
    for i in range(length):
        if i == 0:
            index = random.randint(1, len(ss) - 1)
        else:
            index = random.randint(0, len(ss) - 1)
        ret_str += ss[index]
    return ret_str


# # 日志缓存
# __log_cache = {}
#
# __console_log = None


# 2. init the logging
def init_log(log_file):
    # # 优先从缓存读
    # global __log_cache
    # if log_file in __log_cache:
    #     return __log_cache[log_file]

    LOG_PATH = os.path.dirname(log_file)
    LOG_FILE = os.path.basename(log_file)

    if not os.path.exists(LOG_PATH):
        os.system('mkdir -p %s' % LOG_PATH)

    if not os.path.exists(LOG_FILE):
        os.system('touch %s' % log_file)
        os.system('chmod 666 %s' % log_file)

    fmt = '%(asctime)s %(pathname)s:%(lineno)s [%(levelname)s] - %(message)s'
    formatter = logging.Formatter(fmt)  # 实例化formatter

    handler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight',
                                                        encoding='UTF-8')  # 实例化handler
    handler.setFormatter(formatter)  # 为handler添加formatter
    handler.suffix = '%Y-%m-%d'

    _logger = logging.getLogger('tst')  # 获取名为tst的logger
    _logger.addHandler(handler)  # 为logger添加handler
    _logger.setLevel(logging.DEBUG)

    # sqlalchemy
    # logging.getLogger('sqlalchemy.engine').addHandler(handler)

    # global __console_log
    #
    # if not __console_log:
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    _logger.addHandler(console)
    # __console_log = console

    # logger.info('first info message')
    # logger.debug('first debug message')

    # 放入缓存
    # __log_cache[log_file] = _logger

    return _logger


logger = init_log('/data/logs/moneydb/moneydb.log')


def base64_decode(s):
    return base64.decodestring(s)


def md5(str):
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    str = m.hexdigest()
    return str


def headers_from_str(str, spliter='\n'):
    headers = {}
    for line in str.split(spliter):
        index = line.find(':')
        if index != -1:
            headers[line[:index].strip()] = line[index + 1:].strip()
    return headers


def http_retry(url, method='GET', headers={}, body=None, return_headers=False):
    proto, rest = urllib.splittype(url)
    host, rest = urllib.splithost(rest)

    try:
        conn = httplib.HTTPConnection(host)
        conn.request(method=method, url=url, headers=headers, body=body)
        response = conn.getresponse()
        status = response.status

        while status != 200:
            logger.debug("http_retry status:%d" % status)
            logger.debug("http_retry :%s" % url)
            conn = httplib.HTTPConnection(host)
            conn.request(method=method, url=url, headers=headers, body=body)
            response = conn.getresponse()
            status = response.status

        resp = response.read()
        conn.close()

        if return_headers:
            return response.getheaders(), resp

        return resp
    except:
        logger.exception("http_retry error")
        return http_retry(url, method, headers, body, return_headers)


if __name__ == '__main__':
    # headers = headers_from_str("""
    # Host: gaos.guo7.com
    # Accept: */*
    # Cookie: aliyungf_tc=AQAAACCfSzEYdQEAS0Xhevm8qhYtsk0J
    # User-Agent: QiankaKey/2.0 (iPhone; iOS 8.3; Scale/2.00)
    # Accept-Language: zh-Hans;q=1
    # Connection: keep-alive
    #
    # """)
    #
    # print(headers)
    #
    # s = http_retry(
    #     "http://gaos.guo7.com/zq_api/index.php/lianmeng/ziji?adid=124131&adname=%E6%8E%8C%E4%B8%8A%E7%94%B5%E7%8E%A9%E5%9F%8E&check_click=1&deviceid=5268855F-AA59-4BFE-B64F-61D04F19DE3C&dsid=382080527&mdt=474394876&order=32483806124131&rdl=0&sign=e6e6ccf57a5ddbe78cb30670c76c5611&time=1452702186&ver=1144.17",
    #     headers=headers).decode('unicode-escape')
    # print(s)
    # print(type(s))
    #
    # print(type(base64_decode()))

    # print(gen_uuid())

    # print(time2str(str2time("2016-10-12 23:40:32")))
    # print(nowtime_str())
    # print(after_seconds(60))
    # print(random_str(40))
    # print(type(logger))
    logger.info('sdf')
