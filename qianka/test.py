#!/usr/bin/python
# -*-coding:utf-8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from db import disciple
import httplib

import userinfo
import taskrunner


if __name__ == '__main__':
    # for d in disciple.fetch_all():
    #     cookie=userinfo.login(d['idfa'],d['uuid'],d['userid'])
    #     d['cookie'] = cookie
    #     disciple.update_cookie(d)
    #     try:
    #         userinfo.sync_one_status(d)
    #     except:
    #         print('ignore')

    # print(userinfo.reg_get_user())

    # import myutils
    # print(myutils.gen_uuid())
    # print(myutils.gen_uuid())

    userinfo.batch_gen()
    # userinfo.batch_gen(count=30)
    # userinfo.alipay_withdraw('aliyungf_tc=AQAAAOFZ50kcuQgAhB2Bi5msoqrXzZ5J; PHPSESSID=15b6d58b24031ba9e010260dc292ce8e59a26a32; expires=Mon, 01-Feb-2016 09:34:24 GMT; Max-Age=604800; gaoshou_session=eyJpdiI6ImNNeVdGSXR3OWFFS0hiUTZMTXdXSmc9PSIsInZhbHVlIjoicjlBQXI0VXl3QlFWbnNpZitoR3R4RnNmM09zMzM3OVNmTWZpcHNQb2V0bjB1OGxHXC80N0szdXY5OEQ0NTVLdUhTdDRNbVZNR3YzN01cL0VrcFBWSTVQUT09IiwibWFjIjoiOTgyMzMwYjVhY2ZjZWFlMTUxMzUxYjYyZDkxN2YwMWQyMDcyMGI0ZDEzNGM2OGVhZWZlYWQ4NDljYTMyYTcyZiJ9; expires=Mon, 01-Feb-2016 09:34:24 GMT; Max-Age=604800; path=/; httponly',10)