#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib
import json
import urllib


def headers_from_str(str, spliter='\n'):
    headers = {}
    for line in str.split(spliter):
        index = line.find(':')
        if index != -1:
            headers[line[:index].strip()] = line[index + 1:].strip()
    return headers


def http_retry(url, method='GET', headers={}, body=None, return_headers=False, no_retry=False):
    proto, rest = urllib.splittype(url)
    host, rest = urllib.splithost(rest)

    try:
        conn = httplib.HTTPConnection(host)
        conn.request(method=method, url=url, headers=headers, body=body)
        response = conn.getresponse()
        status = response.status

        max_retry_count = 3
        while status != 200 and not no_retry and max_retry_count > 0:
            conn = httplib.HTTPConnection(host)
            conn.request(method=method, url=url, headers=headers, body=body)
            response = conn.getresponse()
            status = response.status
            max_retry_count -= 1

        resp = response.read()
        conn.close()

        if return_headers:
            return response.getheaders(), resp

        return resp
    except:
        print("http_retry error")


def zebra_common_request(content):
    resp = http_retry('http://zebra.dp/i/sqleditor/executeQuery', method='POST', headers=headers_from_str("""
        Host: zebra.dp
        Connection: keep-alive
        Accept: application/json, text/plain, */*
        Origin: http://zebra.dp
        User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36
        Content-Type: application/json;charset=UTF-8
        Referer: http://zebra.dp/
        Accept-Language: zh-CN,zh;q=0.8,en;q=0.6
        Cookie: ace_settings=%7B%22sidebar-collapsed%22%3A-1%7D; JSESSIONID=F321F4D944432048EB31C25E3CF7B99B; ticket=AAFSsPYAkNKN6Mb0Q6Li8D8gawrtLIcRT1330JSjm2OEpSOsx2YKaaLl; env=product

    """), body=content)

    rows = json.loads(resp)['datas']
    return rows


def query():
    """
    zebra多页查询
    :return:
    """
    max_shop_id = 0

    while True:

        sql = 'select distinct a.shopid  from BeautyContractItem a where a.status = 1 and a.shopid>%d and a.productid in (   10008,10009,111501,111509,111790,111791) order by a.shopid asc limit 10000;' % max_shop_id

        content = '{"ip":"10.1.101.170","port":"3306","database":"BeautyMerchant","sql":"%s"}' % sql

        rows = zebra_common_request(content)

        if len(rows) == 0: break

        max_shop_id = rows[-1][0]
        print(max_shop_id)

        result_str = ''
        for row in rows:
            result_str += str(row[0]) + "\n"

        open('/Users/zhouzhipeng/Documents/20160622-merchantpush/tt.txt', 'a').write(result_str)


if __name__ == '__main__':
    query()
