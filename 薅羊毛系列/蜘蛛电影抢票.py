#!/usr/local/bin/python
# -*-coding:utf-8-*-
# author: zhouzhipeng
# email: admin@zhouzhipeng.com
import hashlib
import urllib.parse
from concurrent.futures import thread

import requests
import time


def gen_url():
    # info_url = 'https://film.spider.com.cn/huayins/getActivityList.html?seqNo=0170100000000000060568222&cinemaId=31074201&operator=CU&sign=4b917476f85b5a0757d069a5903e8161&orderactivity=y&filetype=json&key=huayins&userId=5da71497b4160d20c806c0568e535e07&version=410&filmId=201709909870&type=0&cityCode=shanghai'
    # r = requests.get(info_url)

    # print(r.json())

    # 注意seatId 和 feePrice需要经过两次url decode
    ### 先url解压之后再贴到这里
    url = 'https://film.spider.com.cn/huayins/lockSeatList.html?insBirthday=&insId=&token=D23FC0C4A0656BFCB5961ABB0FC9436C&userId=5da71497b4160d20c806c0568e535e07&hallId=12163&feePrice=2.0%7C2.0&cinemaId=31074201&currentVersion=4.9.1&channelId=sfVivo&appVersion=460&version=410&activityId=101265&showId=0170100000000000061038223&userName=13080669828&partnerPrice=47.00&sign=92563bceb07f5b9fab182d12749d2878&filetype=json&mobile=13080669828&insName=&filmId=201801150207&fpCount=&parorderId=309413156&seatId=6%3A10%7C6%3A9&key=huayins&fpId='

    """
    showId cinemaId hallId filmId userName userId mobile urldecode(seatId) \
    urldecode(feePrice) parorderId channelId partnerPrice activityId insName \
    insBirthday insId fpId fpCount "huayins" "0779257096" token
    """

    """
    "id": "101328",
            "title": "龙卡星期六 5元看电影",
    """

    params = {}
    for p in url.split('?')[1].split('&'):
        params[p.split('=')[0]] = p.split('=')[1]

    # TODO:替换实际的参数值
    activity_id = '101328'
    token = ''  # TODO: 抓包获取登陆token
    # TODO: 需要替换抓包时实际的值 ， 先不用优惠下一次订单

    parorderId='310000428'


    params['activityId']=activity_id
    params['parorderId']=parorderId



    print(params)

    """
    计算 sign 值
    """
    final_str = params['showId'] + params['cinemaId'] + params['hallId'] + params['filmId'] + params['userName'] + \
                params[
                    'userId'] + params['mobile'] + urllib.parse.unquote(params['seatId']) + urllib.parse.unquote(
        params['feePrice']) + \
                params[
                    'parorderId'] + \
                params['channelId'] + params['partnerPrice'] + params['activityId'] + params['insName'] + params[
                    'insBirthday'] + \
                params['insId'] + params['fpId'] + params['fpCount'] + "huayins" + "0779257096" + params[
                    'token']

    print(final_str)


    sign = hashlib.md5(final_str.encode('utf-8')).hexdigest()

    print(sign)

    '''
    将params 拼装为url形式
    '''
    params['sign'] = sign

    new_url = 'https://film.spider.com.cn/huayins/lockSeatList.html?'

    for k in params:
        new_url += k + "=" + params[k] + "&"

    new_url = new_url[:-2]

    print(new_url)
    return new_url


if __name__ == '__main__':
    url = gen_url()

    while True:
        print(requests.get(url).json())
        time.sleep(0.01)
