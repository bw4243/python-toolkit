#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib
import time
import json
import urllib
from myutils import *


#
# list = json.loads(http_retry('http://meta.open.dp/metadata/city/all'))
# map = {}
# for city in list:
#     map[city['cityName']] = city['cityID']
#
# cityids = ''
# for cityname in u'北京、福州、广州、杭州、合肥、宁波、青岛、厦门、上海、深圳、沈阳、苏州、天津、武汉、长沙、郑州、西安、重庆、成都'.split('、'):
#     cityids += str(map[cityname]) + ','
#
# print(cityids)
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


def print_cityids():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    list = json.loads(http_retry('http://meta.open.dp/metadata/city/all'))
    map = {}
    for city in list:
        map[city['cityName']] = city['cityID']
    cityids = ''
    for cityname in u'鞍山 保定 北京 常州 成都 大连 东莞 佛山 福州 抚顺 广州 贵阳 哈尔滨 杭州 合肥 呼和浩特 惠州 济南 嘉兴 昆明 昆山 兰州 临沂 洛阳 南昌 南京 南宁 南通 宁波 青岛 泉州 厦门 上海 绍兴 深圳 沈阳 石家庄 苏州 台州 太原 泰州 唐山 天津 潍坊 温州 无锡 武汉 西安 襄阳 徐州 烟台 扬州 宜昌 义乌 银川 长春 长沙 镇江 郑州 中山 重庆 珠海 淄博'.split(
            ' '):
        cityids += str(map[cityname]) + ','
    #
    print(cityids)


def migrate():
    file = '/Users/zhouzhipeng/Documents/20160308-领券模板二期/backupdata.json'
    prefix_sql = 'INSERT INTO `BonusActivity` (`Id`, `Title`, `HeadImg`, `BtnImg`, `ShareIcon`, `ShareTitle`, `ShareDesc`, `NormalCoupons`, `OtherCoupons`, `AdId`, `StartTime`, `EndTime`, `AlertText`, `BonusEventId`, `RecType`, `Tab1Name`, `Tab1Category`, `Tab1MoreText`, `Tab1MoreLink`, `Tab2Name`, `Tab2Category`, `Tab2MoreText`, `Tab2MoreLink`, `Tab3Name`, `Tab3Category`, `Tab3MoreText`, `Tab3MoreLink`, `ShopName`, `ShopMoreText`, `ShopMoreLink`, `Tab1Topic`, `Tab2Topic`, `Tab3Topic`, `RuleDesc`, `SendCouponType`, `NewUserCoupons`, `AddTime`, `UpdateTime`, `Field1`, `Field2`, `Field3`) VALUES\n'

    insert_sql = ''
    for activity in json.loads(open(file).read())['data']:
        format_str = "(%(Id)d, '%(Title)s', '%(HeadImg)s', '%(BtnImg)s', '%(ShareIcon)s', '%(ShareTitle)s', '%(ShareDesc)s', '%(NormalCoupons)s', '%(OtherCoupons)s', '%(AdId)s', '%(StartTime)s', '%(EndTime)s', '%(AlertText)s', %(BonusEventId)d, %(RecType)d, '%(Tab1Name)s', '%(Tab1Category)s', '%(Tab1MoreText)s', '%(Tab1MoreLink)s', '%(Tab2Name)s', '%(Tab2Category)s', '%(Tab2MoreText)s', '%(Tab2MoreLink)s', '%(Tab3Name)s', '%(Tab3Category)s', '%(Tab3MoreText)s', '%(Tab3MoreLink)s', '%(ShopName)s', '%(ShopMoreText)s', '%(ShopMoreLink)s', '%(Tab1Topic)s', '%(Tab2Topic)s', '%(Tab3Topic)s', '%(RuleDesc)s', %(SendCouponType)d, '%(NewUserCoupons)s', '%(AddTime)s', '%(UpdateTime)s', '%(Field1)s', '%(Field2)s', '%(Field3)s'),"
        activity['NormalCoupons'] = str(activity['NormalCoupon'])
        activity['OtherCoupons'] = str(activity['OtherCoupon'])
        activity['Tab1Topic'] = ''
        activity['Tab2Topic'] = ''
        activity['Tab3Topic'] = ''
        activity['RuleDesc'] = ''
        activity['AdId'] = 'wehavevacation'
        activity['SendCouponType'] = 0 if activity['Field1'] == '' else int(activity['Field1'])
        activity['NewUserCoupons'] = activity['Field2']
        activity['Field1'] = ''
        activity['Field2'] = ''
        activity['Field3'] = ''

        if activity['Id'] == 16:
            activity['RuleDesc'] = u'''
            1、新用户特权：<br>
            （1）可使用20元美发美甲美容优惠券（满20.01元可用），购买团购最低9.9元起，优惠券有效期为7天；<br>
            （2）下单成功还送69元小奥汀甲油一份，每天100份，先到先得，颜色随机，获奖用户将在活动结束后收到系统短信通知；<br>
            *新用户指没有在大众点评购买过美发美甲美容等丽人团购的用户；<br>
            2、所有本活动下单用户都将获小奥汀7折优惠码，活动结束后以系统短信形式发送；<br>
            3、同一点评账号、手机号、设备均视为同一用户，若出现违背上述活动规则、恶意刷单等非正常方式参与活动的行为，大众点评有权取消您的参与活动资格；<br>
            4、活动时间截止至2016年3月13日。
            '''
            activity['Tab1Topic'] = '["18680"]'
            activity['Tab2Topic'] = '["18683"]'
            activity['Tab3Topic'] = '["18684"]'

        row = format_str % activity

        print(row)

        insert_sql += row + '\n'

    insert_sql = prefix_sql + insert_sql[:-2] + ';'

    print(insert_sql)

    open('/Users/zhouzhipeng/Documents/20160308-领券模板二期/migrate_data.sql', 'w').write(insert_sql.encode("UTF-8"))


# migrate()


def mig2(name):
    sql = '''
    INSERT INTO `BeautyCouponCount` (`ShopId`, `SendCount`, `SendTime`, `AddTime`, `UpdateTime`, `SendType`, `TotalCount`, `ContractID`)
VALUES
	(%(ShopId)d, %(SendCount)d, '%(SendTime)s', '%(AddTime)s', '%(UpdateTime)s', %(SendType)d, %(TotalCount)d,  %(ContractID)d);
    '''

    list = json.loads(open('/Users/zhouzhipeng/Documents/20160318-couponcout数据迁移/%s.json' % name).read())['data']

    ss = ''
    for obj in list:
        ss += sql % obj
    print(len(list))
    open('/Users/zhouzhipeng/Documents/20160318-couponcout数据迁移/%s.sql' % name, 'w').write(ss)


def send_push():
    data = ('-8458788633886141025', 'dianping://web?sdfsf', 'testtt2')
    content = 'url=campaign.service.couponCommonService&method=sendAppPush&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s' % data
    resp = http_retry('http://10.1.105.166:4080/invoke.json?' + content, no_retry=True)
    print(resp)


# mig2('13')
# mig2('1500_2')

# print_cityids()

send_push()
