#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib
import time
import json
import urllib

# headers = {
#     "Cookie": "PHPSESSID=0eb0m60mrp8ci21hk4q0jqp9c2",
#     "Content-Type": "application/x-www-form-urlencoded",
# }
# # for k in range(100):
# #     for i in range(1, 9):
# #         time.sleep(0.2)
#
# url = 'http://sobear.elomo.com/WebAPP/index.php/Home/Answer/deal_res'
# conn = httplib.HTTPConnection("sobear.elomo.com")
#
# body = 'rank=3&score=%d&num=10' % 1
#
# headers['Content-Length'] = len(body)
#
# conn.request(method='POST', url=url, headers=headers, body=body)
#
# response = conn.getresponse()
#
# print(response.status)
# print(response.read())
#
# conn.close()


print(json.dumps("abc"))
print(urllib.quote_plus("sdfsdfsdf://"))
print(urllib.quote("sdfsdfsdf://"))


def abc():
    pass

fuck-2
res = urllib.urlopen("sdf")
