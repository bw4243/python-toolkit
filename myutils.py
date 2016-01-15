#!/usr/bin/python
# -*-coding:utf-8-*-
import hashlib
import httplib
import urllib
import base64

def base64_decode():
    return base64.decodestring('LJR1AmH5ZwRjBQtjZTWxMt==')

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


def http_retry(url, method='GET', headers={}, body=None):
    proto, rest = urllib.splittype(url)
    host, rest = urllib.splithost(rest)

    conn = httplib.HTTPConnection(host)
    conn.request(method=method, url=url, headers=headers, body=body)
    response = conn.getresponse()
    status = response.status

    while status != 200:
        print("http_retry status:%d" % status)
        print("http_retry :%s" % url)
        conn = httplib.HTTPConnection(host)
        conn.request(method=method, url=url, headers=headers, body=body)
        response = conn.getresponse()
        status = response.status

    resp = response.read()
    conn.close()
    return resp


if __name__ == '__main__':
    headers = headers_from_str("""
    Host: gaos.guo7.com
    Accept: */*
    Cookie: aliyungf_tc=AQAAACCfSzEYdQEAS0Xhevm8qhYtsk0J
    User-Agent: QiankaKey/2.0 (iPhone; iOS 8.3; Scale/2.00)
    Accept-Language: zh-Hans;q=1
    Connection: keep-alive

    """)

    print(headers)

    s=http_retry(
        "http://gaos.guo7.com/zq_api/index.php/lianmeng/ziji?adid=124131&adname=%E6%8E%8C%E4%B8%8A%E7%94%B5%E7%8E%A9%E5%9F%8E&check_click=1&deviceid=5268855F-AA59-4BFE-B64F-61D04F19DE3C&dsid=382080527&mdt=474394876&order=32483806124131&rdl=0&sign=e6e6ccf57a5ddbe78cb30670c76c5611&time=1452702186&ver=1144.17",
        headers=headers).decode('unicode-escape')
    print(s)
    print(type(s))

    print(type(base64_decode()))
