#!/usr/bin/python
# -*-coding:utf-8-*-

from myutils import *
import json


def set_article(title, content):
    content = 'title=' + title + '&markdowncontent=' + content + '&content=%253Cp%253E' + content + '%253C%252Fp%253E&id=&tags=&description=' + content + '&status=0&level=0&categories=&channel=7&type=original&articleedittype=1'
    resp = http_retry('http://write.blog.csdn.net/mdeditor/setArticle', method='POST', headers=headers_from_str("""
                        Host: write.blog.csdn.net
                        Connection: keep-alive
                        Accept: */*
                        Origin: http://write.blog.csdn.net
                        X-Requested-With: XMLHttpRequest
                        User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36
                        Content-Type: application/x-www-form-urlencoded; charset=UTF-8
                        Referer: http://write.blog.csdn.net/mdeditor
                        Accept-Language: zh-CN,zh;q=0.8,en;q=0.6
                        Cookie: uuid_tt_dd=5518986841215160291_20160513; __utma=17226283.1875965860.1463151175.1463151259.1463151259.1; __utmz=17226283.1463151259.1.1.utmcsr=passport.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/account/login; __message_sys_msg_id=0; __message_gu_msg_id=0; __message_cnel_msg_id=0; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1463151154,1465698604; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1465698604; _ga=GA1.2.1875965860.1463151175; _gat=1; dc_tos=o8n0a9; dc_session_id=1465698609869; _message_m=pj5gfy35ugxmpjugkwja3pen; UserName=smilyboy; UserInfo=B1vuzqq%2B6kws30gMMmPaofrEnbL8IWpRU5dLMvhM6cPih%2BSdNGStV4PvtWUVfwF5c8rerh85H3WrIYCtaVOH1SNFT3fO74SyBxaTFYNo0ik%3D; UserNick=smilyboy; AU=C38; UD=javaer; UN=smilyboy; UE=""; BT=1465698579396; access-token=33f797f0-9982-4909-9050-7e9a95afa201
                        """), body=content)

    print(resp)

    obj = json.loads(resp)
    if obj['status']:
        return obj['data']['url']


if __name__ == '__main__':
    url = set_article('abc', 'hihi')
    print(url)