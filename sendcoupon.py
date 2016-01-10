#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib
import urllib

couponmap = {'1': [13416, 13417, 13418], '2': [13417, 13418], '3': [13418]}

file = open('/Users/zhouzhipeng/Documents/20151118-美甲节/漏券补发.txt', 'r')
for line in file.readlines():
    # print(line)
    arr = line.strip().split('\t')
    userid = arr[0]
    count = arr[1]
    for coupon in couponmap[count]:
        url = 'http://10.1.102.188:8080/cmd?event=ManicureFestival_1&userId=%s&couponGroupIds=%s&time=2:2015-12-04_2015-12-11' % (
            userid, coupon)
        url.replace()
        print(url)

        f = urllib.urlopen(url)
        print f.read()
