#!/usr/bin/python
# -*-coding:utf-8-*-

"""
点评小工具集
"""

import httplib
import time
import json
import urllib
from myutils import *


def print_cityids():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    list = json.loads(http_retry('http://meta.open.dp/metadata/city/all'))
    map = {}
    for city in list:
        map[city['cityName']] = city['cityID']
    cityids = ''
    for cityname in u'鞍山 保定 北京 常州 成都 大连 东莞 佛山 福州 抚顺 广州 哈尔滨 杭州 合肥 呼和浩特 惠州 济南 嘉兴 昆明 兰州 临沂 洛阳 南昌 南京 南宁 南通 宁波 青岛 泉州 厦门 上海 绍兴 深圳 沈阳 石家庄 苏州 台州 太原 泰州 天津 潍坊 温州 无锡 武汉 西安 襄阳 徐州 烟台 扬州 宜昌 义乌 银川 长春 长沙 镇江 郑州 中山 重庆 珠海 淄博'.split(
            ' '):
        cityids += str(map[cityname]) + ','
    #
    print(cityids)


def send_push(dpid, link, text):
    """
    发push
    :param dpid:
    :param link:
    :param text:
    :return:
    """
    # beauty-campaign-service
    content = 'url=campaign.service.couponCommonService&method=sendAppPush&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s' % (
        dpid, link, text)
    print(http_retry('http://10.1.105.166:4080/invoke.json?' + content))


def get_dpid_from_userid(userid):
    """
    从userid查询dpid
    :param userid:
    :return:
    """
    # data-server
    # content = 'url=http://service.dianping.com/dpdata/dpredis&method=get&parameterTypes=java.lang.String&parameters=bi.dprpt_userid_dpid_map.dim&parameterTypes=java.lang.String&parameters=%s' % str(userid)
    # resp=http_retry('http://10.1.106.205:4080/invoke.json?' + content)

    content = 'url=http://service.dianping.com/dpdata/dpuser&method=getUserDpidByUserid&parameterTypes=int&parameters=%s' % (
        userid)
    resp = http_retry('http://10.1.111.112:4080/invoke.json?' + content)
    print(resp)
    return resp


def test():
    ss = u"""
    获得了大众点评丽人88元礼包！
    获得了西十区1000元礼包！
    获得了小红书66元礼包！
    获得了唯品会188元礼包！
    获得了大众点评电影5元礼包！
    获得了大众点评酒店30元礼包！
    获得了西堤厚牛排30元礼包！
    获得了价值599元Dior香水！
    获得了马上诺30元礼包！
    """
    arr = ss.split('\n')
    print(arr)
    name = [u'大', 'B', u'感', u'西', u'萌', u'小', u'啦', u'萝', u'绿', u'咻', u'云', u'想', u'么', 'A', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J', 'L', 'M', 'N', 'O']
    for i in range(200):
        print(name[random.randint(0, len(name) - 1)] + '**' + name[random.randint(0, len(name) - 1)] + arr[
            random.randint(1, len(arr) - 2)])


def youhuicuxiao(accountId, contractID, beginTime, endTime, productId, shopId, itemId):
    """
    优惠促销补数据
    :return:
    """

    privilegeDto = {'orderSource': 0, 'accountId': accountId, 'extOrderId': contractID}
    privilegeitemDto = [
        {'beginTime': beginTime, 'endTime': endTime, 'productId': productId, 'shopId': shopId, 'itemId': itemId}]

    privilegeDto['shtPrivilegeItemDtos'] = privilegeitemDto

    jsonStr = urllib.quote(json.dumps(privilegeDto))

    print(jsonStr)

    content = 'url=http://service.dianping.com/mercahntShopdiyPrivilegeService/shtBaseFunctionService_1.0.0&method=addShtPrivilege&parameterTypes=com.dianping.merchant.shopdiy.privilege.api.dto.ShtPrivilegeDto&parameters=%s' % jsonStr

    print(content)

    resp = http_retry('http://merchant-shopdiy-privilege-service02.nh:4080/invoke.json?' + content)
    print(resp)
    return resp


def set_cache(category, params, value, beta=True):
    """
    设置缓存值
    :param category:
    :param params:
    :param value:
    :return:
    """
    content = 'url=campaign.service.configService&method=setCache&parameterTypes=java.lang.String&parameters=%s&parameterTypes=[Ljava.lang.Object;&parameters=%s&parameterTypes=java.lang.Object&parameters=%s' % (
        category, str(params), value)
    print(content)
    resp = http_retry('http://%s:4080/invoke.json?%s' % (
        ['beauty-campaign-service02.nh', 'beauty-campaign-service01.beta'][beta], content))
    print(resp)


def get_cache(category, params, beta=True):
    """
    获取缓存值
    :param category:
    :param params:
    :return:
    """
    content = 'url=campaign.service.configService&method=getCache&parameterTypes=java.lang.String&parameters=%s&parameterTypes=[Ljava.lang.Object;&parameters=%s' % (
        category, str(params))
    print(content)
    resp = http_retry('http://%s:4080/invoke.json?%s' % (
        ['beauty-campaign-service02.nh', 'beauty-campaign-service01.beta'][beta], content))
    print(resp)
    return resp


def is_new_user(userid, sort_type='site', mobile='', dpid='', beta=False):
    """
    判断是否是某平台新用户
    :param userid:
    :param sort_type: site-全站,bu50-丽人
    :param mobile:
    :param dpid:
    :return:
    """

    servers = ['dpuser-service01.beta', 'dpuser-service04.nh']

    content = 'url=http://service.dianping.com/dpdata/dpuser&method=isFirstBuyUser&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s' % (
        userid, sort_type, mobile, dpid)
    print(content)
    resp = http_retry('http://%s:4080/invoke.json?%s' % (servers[beta], content))
    print(resp)
    return resp


def fix_youhui_data():
    """
    批量补优惠促销配置数据
    :return:
    """
    obj = json.loads(open('/Users/zhouzhipeng/Documents/contract.txt').read())
    for item in obj['data']:
        begin, end = item['duration'].split('-')
        begin_str = datetime.datetime.strptime(begin, '%Y%m%d%H%M%S').strftime('%Y-%m-%dT%H:%M:%S.000+0800')
        end_str = datetime.datetime.strptime(end, '%Y%m%d%H%M%S').strftime('%Y-%m-%dT%H:%M:%S.000+0800')

        youhuicuxiao(accountId=item['accountId'], contractID=item['contractID'], beginTime=begin_str, endTime=end_str,
                     productId=item['productId'],
                     shopId=item['shopId'], itemId=item['itemId'])


def home_pic_data():
    '''
    未开通的门店主图的数据获取
    :return:
    '''

    # select distinct accountid,customerid from BeautyContractItem  as A where A.status=1 and A.accountid!=0 and  A.shopid not in (select distinct shopid from HomePagePic);
    # obj = json.loads(open('/Users/zhouzhipeng/Documents/data.json').read())

    obj = json.loads(open('/Users/zhouzhipeng/Documents/data_whole.json').read())

    normal_accounts = []
    admin_accounts = []

    whole_str = ''

    for item in obj['data']:

        try:

            accountid = str(item['accountid'])
            customerid = str(item['customerid'])

            print(item)

            # 1.判断是否管理员
            resp = http_retry(
                'http://merchant-member-rpc-service01.nh:4080/invoke.json?validate=false&direct=false&token=&parameters%5B%5D=' + accountid + '&url=http%3A%2F%2Fservice.dianping.com%2FmerchantService%2FuserAuthoriseService_1.0.0&method=loadAccountDetailInfo&parameterTypes%5B%5D=int')

            is_admin = False

            if resp:
                is_admin = json.loads(resp)['userAdmin']

            whole_str += accountid + '\t' + str(item['shopid']) + '\t' + str(is_admin) + '\n'

            if not is_admin:
                normal_accounts.append(str(accountid))

                # 查询管理员账号
                resp = http_retry(
                    'http://merchant-member-rpc-service01.nh:4080/invoke.json?validate=false&direct=false&token=&parameters%5B%5D=[' + customerid + ']&url=http%3A%2F%2Fservice.dianping.com%2FmerchantService%2FuserAuthoriseService_1.0.0&method=getAdminIdsByCustomerIds&parameterTypes%5B%5D=java.util.List')

                ret = json.loads(resp)
                if str(customerid) in ret:
                    admin_account_id = ret[str(customerid)]
                    admin_accounts.append(str(admin_account_id))

                    whole_str += str(admin_account_id) + '\t' + str(item['shopid']) + '\t' + str(True) + '\n'

            else:
                admin_accounts.append(str(accountid))

        except:
            print("error=====")
            print(item)
    # print(set(admin_accounts))
    # print(set(normal_accounts))

    open('/Users/zhouzhipeng/Documents/admin_accounts.txt', 'w').write('\n'.join(set(admin_accounts)))
    open('/Users/zhouzhipeng/Documents/normal_accounts.txt', 'w').write('\n'.join(set(normal_accounts)))
    open('/Users/zhouzhipeng/Documents/whole_data.txt', 'w').write(whole_str)


def find_shop_infos():
    """
    查询店铺信息通过accountid
    :return:
    """
    result = ''
    obj = open('/Users/zhouzhipeng/Downloads/accountids.txt').read().split('\r')
    for account_id in obj:
        account_id = account_id.strip()
        if account_id == '':
            continue
        resp = http_retry(
            'http://merchant-member-rpc-service01.nh:4080/invoke.json?validate=false&direct=false&token=undefined&parameters%5B%5D=' + str(
                account_id) + '&url=http%3A%2F%2Fservice.dianping.com%2FmerchantService%2FuserAuthoriseService_1.0.0&method=fetchAllShopIdsByShopAccountId&parameterTypes%5B%5D=int')
        shopids = json.loads(resp)
        for shopid in shopids:
            try:
                resp = http_retry(
                    'http://shop-server28.nh:4080/invoke.json?validate=false&direct=false&token=&parameters%5B%5D=' + str(
                        shopid) + '&url=http%3A%2F%2Fservice.dianping.com%2FshopService%2FshopService_2.0.0&method=loadShop&parameterTypes%5B%5D=int')

                resp = json.loads(resp)
                shopname = resp['shopName'].encode('utf-8')
                shoptype = resp['shopType'] == 50
                result = str(account_id) + '\t' + str(shopid) + '\t' + shopname + '\t' + str(shoptype) + '\r'
                open('/Users/zhouzhipeng/Downloads/results.txt', 'a').write(result)

            except:
                print("error:" + account_id)




def find_account_infos():
    """
    通过门店信息查询账户
    :return:
    """

    obj = open('/Users/zhouzhipeng/Downloads/shopids.txt').read().split('\n')
    for shopid in obj:
        resp = http_retry(
            'http://merchant-member-rpc-service01.nh:4080/invoke.json?validate=false&direct=false&token=undefined&parameters%5B%5D=' + str(
                shopid) + '&url=http%3A%2F%2Fservice.dianping.com%2FmerchantService%2FuserAuthoriseService_1.0.0&method=fetchAllShopAccountIdByShopId&parameterTypes%5B%5D=int')
        accountids = json.loads(resp)
        result = ''
        for accountid in accountids:
            result+=str(accountid)+"\n"

        try:
            open('/Users/zhouzhipeng/Downloads/accountids_results.txt', 'a').write(result)
        except:
            print("error:" + shopid)


def load_misc_data():
    """
    商户通场景化push 历史数据清洗
    :return:
    """
    # result=''
    # obj = open('/Users/zhouzhipeng/Documents/20160622-merchantpush/PK0620.csv').read().split('\r')
    # for account_id in obj:
    #     account_id=account_id.strip()
    #     resp=http_retry('http://merchant-member-rpc-service01.nh:4080/invoke.json?validate=false&direct=false&token=undefined&parameters%5B%5D='+str(account_id)+'&url=http%3A%2F%2Fservice.dianping.com%2FmerchantService%2FuserAuthoriseService_1.0.0&method=fetchAllShopIdsByShopAccountId&parameterTypes%5B%5D=int')
    #     shopids=json.loads(resp)
    #     for shopid in shopids:
    #         try:
    #             resp=http_retry('http://shop-server28.nh:4080/invoke.json?validate=false&direct=false&token=&parameters%5B%5D='+str(shopid)+'&url=http%3A%2F%2Fservice.dianping.com%2FshopService%2FshopService_2.0.0&method=loadShop&parameterTypes%5B%5D=int')
    #             shopname=json.loads(resp)['shopName'].encode('utf-8')
    #             result+=str(account_id)+'\t'+ str(shopid)+'\t'+shopname+'\r'
    #
    #         except:
    #             print("error:"+account_id)
    #
    # open('/Users/zhouzhipeng/Downloads/PK0620_shops.txt','w').write(result)
    load_contract_data()
    load_album_data()
    load_booking_data()
    load_homepage_data()
    load_product_data()


def load_contract_data():
    """
    load合同中的accountid 和shopid
    :return:
    """
    max_shop_id = 0

    while True:

        sql = 'select distinct accountid,shopid from BeautyContractItem where accountid !=0 and shopid !=0 and shopid> %d  order by shopid asc limit 10000;' % max_shop_id
        content = '{"ip":"10.1.101.170","port":"3306","database":"BeautyMerchant","sql":"%s"}' % sql

        rows = zebra_common_request(content)

        if len(rows) == 0: break

        max_shop_id = rows[-1][1]
        print(max_shop_id)

        result_str = ''
        for row in rows:
            result_str += str(row[0]) + "," + str(row[1]) + "\n"

        open('/Users/zhouzhipeng/Documents/20160622-merchantpush/contract_data.txt', 'a').write(result_str)


def load_homepage_data():
    """
    load门店主图shopid
    :return:
    """
    max_shop_id = 0

    while True:

        sql = 'select distinct(shopid) from HomePagePic where  shopid !=0 and shopid> %d  order by shopid asc  limit 10000;' % max_shop_id
        content = '{"ip":"10.1.101.170","port":"3306","database":"BeautyMerchant","sql":"%s"}' % sql

        rows = zebra_common_request(content)

        if len(rows) == 0: break

        max_shop_id = rows[-1][0]
        print(max_shop_id)

        result_str = ''
        for row in rows:
            result_str += str(row[0]) + "\n"

        open('/Users/zhouzhipeng/Documents/20160622-merchantpush/homepic_data.txt', 'a').write(result_str)


def load_booking_data():
    """
    load 预约shopid
    :return:
    """
    max_shop_id = 0

    while True:

        sql = 'select distinct(shopid) from VC_BookShop where rootcategoryid=50 and   shopid !=0  and shopid> %d order by shopid asc limit 10000;' % max_shop_id
        content = '{"ip":"10.1.101.170","port":"3306","database":"DianPingVC","sql":"%s"}' % sql

        rows = zebra_common_request(content)

        if len(rows) == 0: break

        max_shop_id = rows[-1][0]
        print(max_shop_id)

        result_str = ''
        for row in rows:
            result_str += str(row[0]) + "\n"

        open('/Users/zhouzhipeng/Documents/20160622-merchantpush/booking_data.txt', 'a').write(result_str)


def load_product_data():
    """
    load 产品服务shopid
    :return:
    """
    max_shop_id = 0

    while True:

        sql = 'select distinct(shopid) from VC_BookProduct where BookType=1 and Status in (1,2,3)  and shopid!=0 and shopid> %d  order by shopid asc limit 10000;' % max_shop_id
        content = '{"ip":"10.1.101.170","port":"3306","database":"DianPingVC","sql":"%s"}' % sql

        rows = zebra_common_request(content)

        if len(rows) == 0: break

        max_shop_id = rows[-1][0]
        print(max_shop_id)

        result_str = ''
        for row in rows:
            result_str += str(row[0]) + "\n"

        open('/Users/zhouzhipeng/Documents/20160622-merchantpush/product_data.txt', 'a').write(result_str)


def load_album_data():
    """
    load 官方相册shopid
    :return:
    """
    max_shop_id = 0

    while True:

        sql = 'select distinct(shopid) from Post where Status in (0,2,3,5) and OfficialType!=0 and shopid!=0 and shopid> %d  order by shopid asc limit 10000;' % max_shop_id
        content = '{"ip":"10.1.101.170","port":"3306","database":"BeautyZone","sql":"%s"}' % sql

        rows = zebra_common_request(content)

        if len(rows) == 0: break

        max_shop_id = rows[-1][0]
        print(max_shop_id)

        result_str = ''
        for row in rows:
            result_str += str(row[0]) + "\n"

        open('/Users/zhouzhipeng/Documents/20160622-merchantpush/album_data.txt', 'a').write(result_str)


def load_test():
    # select distinct shopid from BeautyContractItem where productid=111563 and status=2 and shopid!=0  and shopid> %d order by shopid asc  limit 10000;
    """
    load 官方相册shopid
    :return:
    """
    max_shop_id = 0
    open('/Users/zhouzhipeng/Documents/testshops.txt', 'w').write('')

    while True:

        sql = "select distinct shopid from BeautyContractItem where status=1 and shopid!=0  and shopid> %d order by shopid asc limit 10000;" % max_shop_id
        content = '{"ip":"10.1.101.170","port":"3306","database":"BeautyMerchant","sql":"%s"}' % sql

        rows = zebra_common_request(content)

        if len(rows) == 0: break

        max_shop_id = rows[-1][0]
        print(max_shop_id)

        result_str = ''
        for row in rows:
            result_str += str(row[0]) + "\n"

        open('/Users/zhouzhipeng/Documents/testshops.txt', 'a').write(result_str)


def zebra_common_request(content):
    resp = http_retry('http://rds.dp/i/sqleditor/executeQuery', method='POST', headers=headers_from_str("""
        Host: zebra.dp
        Connection: keep-alive
        Accept: application/json, text/plain, */*
        Origin: http://zebra.dp
        User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36
        Content-Type: application/json;charset=UTF-8
        Referer: http://zebra.dp/
        Accept-Language: zh-CN,zh;q=0.8,en;q=0.6
        Cookie: ticket=AAFSsPYAkNKN6Mb0Q6Li8D8gawrtLCTsKvuB8l4EegnfzWnjwfcHePhm

    """), body=content)

    rows = json.loads(resp)['datas']
    return rows


def init_bizproperty():
    # 1.读取个场景中的数据
    homepage_shopids = open('/Users/zhouzhipeng/Documents/20160622-merchantpush/homepic_data.txt', 'r').read().split(
        '\n')
    booking_shopids = open('/Users/zhouzhipeng/Documents/20160622-merchantpush/booking_data.txt', 'r').read().split(
        '\n')
    product_shopids = open('/Users/zhouzhipeng/Documents/20160622-merchantpush/product_data.txt', 'r').read().split(
        '\n')
    album_shopids = open('/Users/zhouzhipeng/Documents/20160622-merchantpush/album_data.txt', 'r').read().split('\n')

    account_detail_cache = {}

    duplicatcat = []

    # 2.先读取合同中的accountid和shopid
    result_sql = 'insert into AccountBizProperty(AccountId,CustomerId,ShopId,BinaryFlags,Field1,AddTime) values \n'
    for row in open('/Users/zhouzhipeng/Documents/20160622-merchantpush/contract_data.txt', 'r').read().split('\n'):
        if row.strip() == '': continue

        if row in duplicatcat:
            continue

        duplicatcat.append(row)

        accountid, shopid = row.split(',')

        # 判断flag标志
        # MainPic(1, "门店主图"),
        # Album(2, "官方相册"),
        # Product(4, "服务项目"),
        # Booking(8, "预约功能");

        BinaryFlags = 0

        if shopid in homepage_shopids:
            BinaryFlags += 1
        if shopid in album_shopids:
            BinaryFlags += 2
        if shopid in product_shopids:
            BinaryFlags += 4
        if shopid in booking_shopids:
            BinaryFlags += 8

        customerid = 0
        Field1 = 0

        # try:
        #     if accountid in account_detail_cache:
        #         customerid,Field1=account_detail_cache[accountid]
        #     else:
        #         #判断accountid是否是管理员
        #         detail= json.loads(http_retry('http://merchant-member-rpc-service01.nh:4080/invoke.json?validate=false&direct=false&token=&parameters%5B%5D='+str(accountid)+'&url=http%3A%2F%2Fservice.dianping.com%2FmerchantService%2FuserAuthoriseService_1.0.0&method=loadAccountDetailInfo&parameterTypes%5B%5D=int'))
        #
        #         if detail and detail['userAdmin']:
        #             customerid=detail['merchantId']
        #             if customerid >0 :
        #                 #查询管理员账号
        #                 try:
        #                     detail= json.loads(http_retry('http://merchant-member-rpc-service01.nh:4080/invoke.json?validate=false&direct=false&token=&parameters%5B%5D='+str(customerid)+'&url=http%3A%2F%2Fservice.dianping.com%2FmerchantService%2FuserAuthoriseService_1.0.0&method=getCustomerAdminUser&parameterTypes%5B%5D=int'))
        #                 except:
        #                     pass
        #                 if detail:
        #                     Field1=detail['shopAccountId']
        #                     account_detail_cache[accountid]=(customerid,Field1)
        # except:
        #     print("error accountid:"+accountid)
        #     account_detail_cache[accountid]=(0,0)


        result_sql += "(%s,%s,%s,%s,%s,'%s'),\n" % (
        str(accountid), str(customerid), str(shopid), str(BinaryFlags), str(Field1), '2016-06-2 00:00:00')

    result_sql = result_sql[:-2] + ';'
    open('/Users/zhouzhipeng/Documents/20160622-merchantpush/biz_property_result.txt', 'w').write(result_sql)


def test():
    """
    load 官方相册shopid
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


def sso_login():
    content = 'username=zhipeng.zhou&password=*******&token=&lt=LT-45028798-UNprlTJIjRCqSkycTkGe&execution=3252b4e3-e697-4e5b-940d-ce91c336f1bf_AAAAHgAAAAw8hNB7cDSaFwj9T8IAAAAGYWVzMTI4Auaq1GmTMG8Kmh7yP8mh4+JOFUQK65+McbPO7K7OMejWY0NSbm87BIwbEF3BRLONdByy63m1oXP09Ox9JvlZC6VUklwdGjTGi/xQvjI0nJrB9Im8AfD+WRFV2K34zF4UmpjZWhVTGj/VGf4vUpEDCiw1M+n9Y79gUjt1pI18R/JJaiBhWsiG64A01gY5Wvll+O9u/c94AET/0qZ7ZWvtNyS7WUBHh1PFXpL1QlNIQ1h8W2ZctQX7yXJt2vPIykligF2IU5Ryq9dvObQV5l1EnS/l62ENijtT4VF7hTCLa3XuXLSt+PL6A30dyTNwm1LxsI3cNYB/P5V0R5ctfb21Re7CLe3/vMWyHg2YTMwUy22x2N1mb8hzFkA5zKZcvZI4QtlF3qHpWOXYe35W8ewfCryRtNYpw5sX92O/DTu+bARv7QkSlU8zEfC/BTPkB6AMOZyOw4SUlnP/18RAGu0HwlD3bm4pStru9wQkD6K5fToEEISqDxntZha6GIDUvD3SnBACKz49u0LGG5u+9ZsoA6KJGwDpE4co2iATjArynu/iBy+b2XKvDXRksi70AcQGHa7iLkFxvSeE8aIv/9HZ+Mwi21uvJnjvAXxUtPohMQf5/VqgzHco/ULig0vIwRblHunU7i/TwmEI1yR6eKgneZg3vcpNumENbQ7HuHNuzL2HzWusWdLdzCwZRyroHPp4wAmWwEEupuTsc4Ohxz2tvkD0Ep+xmbUxp3KQRkjwWs1qRgYt0z5pywkhu29aMK1Rv1WX7G0as8/NMI3YMDwGtE6UulyF5eCH8BpdGQe/GOM4ec3tlVzzZ6wPZv+Rs/AT0Cjg/+/y3GY2YabmpbyVnSSfBCspm0hpfZtkyl8Kq6VQ+zHlJ/mMFWrZGi3/3j049SMUu9ZMsa74PG6OVpA2uVY7pSI063lEdwHK7inECz20OTJYkl5j6/D13+Y9C/keTO6QSQDpGE2iEPLbRtEiulLrRIG66rBt1Bhm3e3rKLE9UEFolQlWlwUGOAnuDvmcrAG0K0ICmbAScUVhfKR1xky+VkBZnQkkhwJs84QvbyNS97fjOwk9Q0x7pE3pW8nZo9nl+FKkx/Lifi9BEBig0TT75INRiCRtHra5d6PbryNlH89nkMh0ScQPrtewew+GobN/QZCFSyMiWRqmzBBGoWf59FutHrFS4qhZJI/3SEMknMmaDwD7PXupbsoHWr65+8FeOcykwIKC+YwKLfLl15pNxbPGjZ9rGonxnYKi5u9zC9Nw3NCFqhZNltsiEOSjRzfjnM33LyDdfuzTyOVkTZRLBLz8FknpdtfrMspm4csB7AGzY8+mFQplrDqBijVTE3sAHsSgnyrR8eg2/rV/1hPADxzkDczEWoRbJLN5QKnOgoQi67uVwZZ/BulZqvbckMA6Wit4rd48G9rjDOZBMZ3C2tZwQeGJzAkBhmWR+GcCC17hKdQJS+gs8fUefAR1BmZOdEj7XY7VENwWGOMcn1ruWcmHTjIlXxrwPvTvkr3vWo1eyp088hjxMfWOJaR317MInv8HDA==&_eventId_submit=%E7%99%BB+%E5%BD%95&_eventId_submit=%E7%99%BB+%E5%BD%95'
    headers, resp = http_retry('https://sso.dper.com/login?TARGET=http%3A%2F%2Frds.dp%2F',
                               method='POST', headers=headers_from_str("""
                Host: sso.dper.com
                Connection: keep-alive
                Cache-Control: max-age=0
                Origin: https://sso.dper.com
                User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36
                Content-Type: application/x-www-form-urlencoded
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
                Referer: https://sso.dper.com/login?TARGET=http%3A%2F%2Frds.dp%2F
                Accept-Language: zh-CN,zh;q=0.8,en;q=0.6
               """), body=content, return_headers=True, no_retry=True)

    print(headers)
    print(resp)


def getOrderIdFromContractNo(contractNo):
    sql = "SELECT orderId FROM `MLC_OrderBaseInfo` WHERE `contractNo` = '%s' LIMIT 1" % contractNo
    content = '{"ip":"10.3.10.54","port":"3306","database":"DianPingMidas","sql":"%s"}' % sql

    rows = zebra_common_request(content)

    print(rows[0][0])
    return rows[0][0]


def fixContractData(contractNo):
    orderid = getOrderIdFromContractNo(contractNo)
    resp = http_retry('http://beauty-merchant-service01.nh:4080/invoke.json?validate=false&parameters%5B%5D=' + str(
        orderid) + '&url=beauty.merchant.BeautyMerchantContractItemService&method=fixDataAuto&parameterTypes%5B%5D=int')
    print(resp)

def fixContractDataByOrderId(orderid):
    resp = http_retry('http://beauty-merchant-service01.nh:4080/invoke.json?validate=false&parameters%5B%5D=' + str(
        orderid) + '&url=beauty.merchant.BeautyMerchantContractItemService&method=fixDataAuto&parameterTypes%5B%5D=int')
    print(resp)


def checkorderid():
    """
    检查遗漏的合同
    :return:
    """
    max_shop_id = 0

    open('/Users/zhouzhipeng/Documents/orders.txt', 'w').write('')

    while True:

        sql = "select distinct orderid from MLC_OrderBaseInfo where addTime between '2016-06-01 00:00:00' and '2016-07-01 00:00:00' and status=1 and orderid>%d order by orderid asc limit 10000;" % max_shop_id
        content = '{"ip":"10.3.10.54","port":"3306","database":"DianPingMidas","sql":"%s"}' % sql

        rows = zebra_common_request(content)

        if len(rows) == 0: break

        max_shop_id = rows[-1][0]
        print(max_shop_id)

        result_str = ''
        for row in rows:
            result_str += str(row[0]) + "\n"

        open('/Users/zhouzhipeng/Documents/orders.txt', 'a').write(result_str)

def fixAllOrders():
    orderids=open('/Users/zhouzhipeng/Documents/orders.txt', 'r').read().split('\n')
    for orderid in orderids:
        if orderid.strip():
            fixContractDataByOrderId(orderid)


if __name__ == '__main__':
    # sso_login()
    # fixContractData('ADE041887')
    # checkorderid()
    # checkorderid()
    # fixAllOrders()

    #优惠促销手动补数据
    # youhuicuxiao(3662138,9275726,'2016-07-01T00:00:00.000+0800','2016-12-31T23:59:59.000+0800',111790,57086239,11264420)
    # load_test()
    find_account_infos()
    pass
