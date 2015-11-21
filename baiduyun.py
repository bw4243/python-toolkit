#!/usr/bin/python
# -*-coding:utf-8-*-

"""
百度云盘下载/上传工具
"""

import httplib
import json
import urllib
from sgmllib import SGMLParser
import re
import socket

headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
    'Referer': 'http://pan.baidu.com/disk/home',
    'Accept-Language': 'zh-CN,zhq=0.8,enq=0.6',
    'Cookie': 'PANWEB=1; bdshare_firstime=1431516020284; Hm_lvt_b181fb73f90936ebd334d457c848c8b5=1438940732,1439791116; BDUSS=2lxLXBBVlpteFdDQUJQOFMxR2FSaDkzU35WeEdsTFVTN2JEdjBKbTFDRzZRRHRXQVFBQUFBJCQAAAAAAAAAAAEAAAAXxAYXzOy5-tauwbUwMQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALqzE1a6sxNWM; Hm_lvt_eb77799942fcf84785b5626e398e49ab=1443681127,1445700567; windows=undefined; BDCLND=knieuGNYTjE0l%2Bpw%2Fy8Y%2FkWzctcUm5D%2FuXO1d2qr7M8%3D; BAIDUID=EAD93A351A735C3BD3F343B436C43BDE:FG=1; BIDUPSID=96983B253DBBB70DC0FA3325B5B818F5; PSTM=1447294979; H_PS_PSSID=17870_1468_17231_17901_17946_17783_17927_10211_17971_18042_17000_17073_15568_11483_14550_10632; PANPSC=18279089924271893191%3A9qIJoSpryQ8Hcs8JohSjN%2Bn90oj%2BY%2FIsVjzUp5W3kI77%2FZK1BW9FBtjsfRBhJBH7ZL8jhHrk0tp4F6H61hEiOGykL7U5mC5ue32KzRF3PhmtUq%2FdzxBw4suZtTtfbRVi8BKojHWRX7CP3OZ6iXfgEknOysGAv%2BpK5qUnBZ6Hwuc%2BLc0qtRqU313r50aC2wG7K1POGQkWDpH1LyVDippWBH5IlZf3%2F0X8iS3u8yDNz5M%3D; Hm_lvt_adf736c22cd6bcc36a1d27e5af30949e=1447408667,1447431266,1447572691,1447725986; Hm_lpvt_adf736c22cd6bcc36a1d27e5af30949e=1447819617; Hm_lvt_773fea2ac036979ebb5fcc768d8beb67=1447408667,1447431266,1447572691,1447725986; Hm_lpvt_773fea2ac036979ebb5fcc768d8beb67=1447819617',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'

}


def getSignAndTimestamp():
    def base64_encode(str):
        base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        i = 0
        length = len(str)
        string = ''

        while i < length:
            c1 = ord(str[i]) & 0xff
            i += 1
            if i == length:
                string += base64EncodeChars[(c1 >> 2)]
                string += base64EncodeChars[((c1 & 0x3) << 4)]
                string += "=="
                break
            c2 = ord(str[i])
            i += 1
            if i == length:
                string += base64EncodeChars[(c1 >> 2)]
                string += base64EncodeChars[(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4))]
                string += base64EncodeChars[((c2 & 0xF) << 2)]
                string += "="
                break
            c3 = ord(str[i])
            i += 1
            string += base64EncodeChars[(c1 >> 2)]
            string += base64EncodeChars[(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4))]
            string += base64EncodeChars[(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6))]
            string += base64EncodeChars[(c3 & 0x3F)]

        return string

    def sign2(j, r):
        a = []
        p = []
        o = ""
        v = len(j)
        for q in range(0, 256):
            a.append(ord(j[(q % v):((q % v) + 1)][0]))
            p.append(q)

        u = 0
        for q in range(0, 256):
            u = (u + p[q] + a[q]) % 256
            t = p[q]
            p[q] = p[u]
            p[u] = t

        i = u = 0
        for q in range(0, len(r)):
            i = (i + 1) % 256
            u = (u + p[i]) % 256
            t = p[i]
            p[i] = p[u]
            p[u] = t
            k = p[((p[i] + p[u]) % 256)]
            o += chr(ord(r[q]) ^ k)

        print(o)

        return o



    conn = httplib.HTTPConnection("pan.baidu.com")
    conn.request(method="GET", url='/disk/home', headers=headers)
    response = conn.getresponse()

    print(response.status)
    if response.status == 200:
        html = response.read()
        # print(html)
        yunData = {}
        for line in re.findall('yunData\..+= [\'"].+[\'"]', html):
            if 'sign2' not in line:
                ss = line.split('=')
                yunData[ss[0].strip().split('.')[1]] = ss[1].strip()[1:-1]

        sign = base64_encode(sign2(yunData['sign3'], yunData['sign1']))
        return {'timestamp': yunData['timestamp'], 'sign': sign}


def getfid(path, filename):
    # %2Fpenkie_sync
    # path = path.decode('gbk', 'replace')
    path = urllib.quote_plus(path)
    filename = filename.decode('utf-8')

    print(path)

    url = 'http://pan.baidu.com/api/list?channel=chunlei&clienttype=0&web=1&num=100&page=1&dir=' + path + '&order=time&desc=1&showempty=0&_=1447826869074&bdstoken=deeff860004d2acef59ad05ee8657b8a&channel=chunlei&clienttype=0&web=1&app_id=250528'
    conn = httplib.HTTPConnection("pan.baidu.com")
    conn.request(method='GET', url=url, headers=headers)

    response = conn.getresponse()

    print(response.status)

    if response.status == 200:
        result = response.read()
        print(result)
        obj = json.loads(result)
        if obj['errno'] == 0:
            for file in obj['list']:
                if file['isdir'] == 0 and file['server_filename'] == filename:
                    return file['fs_id']


def getDlink(fid, sign, timestamp):
    fid = str(fid)
    timestamp = str(timestamp)
    sign = urllib.quote(sign)

    url = 'http://pan.baidu.com/api/download?sign=' + sign + '&timestamp=' + timestamp + '&fidlist=%5B' + fid + '%5D&type=dlink&bdstoken=deeff860004d2acef59ad05ee8657b8a&channel=chunlei&clienttype=0&web=1&app_id=250528'
    conn = httplib.HTTPConnection("pan.baidu.com")
    conn.request(method='GET', url=url, headers=headers)

    response = conn.getresponse()

    print(response.status)

    if response.status == 200:
        result = response.read()
        print(result)
        obj = json.loads(result)
        if obj['errno'] == 0:
            return obj['dlink'][0]['dlink']


def getRealDownloadUrl(dlink):
    # cflg=65151%3A3,cflg=127%3A3
    conn = httplib.HTTPConnection('d.pcs.baidu.com')
    conn.request(method="GET", url=dlink , headers=headers)
    response = conn.getresponse()

    print(response.status)
    print(response.read())
    print(response.getheaders())

    downloadUrl = ''
    while (response.status == 302):
        downloadUrl = response.getheader("location")
        arr = urllib.splithost(urllib.splittype(downloadUrl)[1])
        host = arr[0]

        conn = httplib.HTTPConnection(host)
        conn.request(method="HEAD", url=arr[1], headers=headers)

        response = conn.getresponse()
        print(response.status)
        # print(response.read())
        print(response.getheaders())

    return downloadUrl


    # if response.status == 200:
    #     json_str = response.read()
    #     print(json_str)
    #     ret = json.loads(json_str)
    #     if ret["errno"] == 0:
    #         download_url = ret["dlink"][0]["dlink"]
    #         print(download_url)
    # {"errno":112,"request_id":7435144554096047255} sign过期
    # -1 下载的文件包含违章信息
    # return 2 == t && (r = "下载失败，请稍候重试"),
    # t && (r = r || e.ErrorMessage[t]),
    # 116 === t && (r = "该分享不存在！"),
    # -1 === t && (r = "您下载的内容中包含违规信息！"),
    # 118 === t && (r = "没有下载权限！"),
    # 113 === t && (r = '页面已过期，请<a href="javascript:window.location.reload()">刷新</a>后重试'),
    # -20 === t ? void this._getcaptcha(function(t) {
    #     n._showVerifyDialog(t.vcode_img, t.vcode_str)
    # }) : (121 === t && (r = "你选择操作的文件过多，减点试试吧。"), r = r || "网络错误，请稍候重试", void a.obtain.useToast({
    #     toastMode: a.obtain.MODE_CAUTION,
    #     msg: r,
    #     sticky: !1
    # }))


def download():
    # fid=getfid("/penkie_sync",'sync.txt')
    # fid=getfid("/ts视频播放器/mac版本",'vlc-2.2.1.dmg')
    fid = getfid("/游戏素材", '三国杀.rar')

    if fid == None:
        print(">>>获取fid出错啦!!")
        return

    map = getSignAndTimestamp()

    if map == None:
        print(">>>获取getSignAndTimestamp出错啦!!")
        return

    dlink = getDlink(fid, map['sign'], map['timestamp'])

    if dlink == None:
        print(">>>获取dlink出错啦!!")
        return

    print(dlink)

    downloadUrl = getRealDownloadUrl(dlink)

    print(downloadUrl)

    if downloadUrl == None:
        print(">>>获取downloadUrl出错啦!!")
        return


# download()


# 上传到云盘
def upload(path,filename):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("c.pcs.baidu.com", 80))
    s.sen





