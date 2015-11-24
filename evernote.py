#!/usr/bin/python
# -*-coding:utf-8-*-

# 印象笔记小工具，用于第三方创建笔记

import httplib, re
from sgmllib import SGMLParser
import urllib
from xml.etree import ElementTree
import os


def __login():
    headers = {
        "Host": "app.yinxiang.com",
        "Connection": "keep-alive",
        "Origin": "https://app.yinxiang.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": "https://app.yinxiang.com/Home.action",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6"
    }

    conn = httplib.HTTPSConnection("app.yinxiang.com")
    conn.request(method="POST", url="/Login.action", headers=headers)

    response = conn.getresponse()

    print(response.status)
    print(response.getheaders())
    # print(response.read())
    html = response.read()

    conn.close()

    # print(html)


    # 解析参数
    hpts = re.findall('document\.getElementById\("hpts"\)\.value = ".+";', html)[0].split("=")[1][2:-2]
    hptsh = re.findall('document\.getElementById\("hptsh"\)\.value = ".+";', html)[0].split(".value")[1][4:-2]

    class ListName(SGMLParser):
        def __init__(self):
            SGMLParser.__init__(self)
            self.map = {}

        def start_input(self, attrs):

            if ("name", "_sourcePage") in attrs and "_sourcePage" not in self.map:
                for item in attrs:
                    if (item[0] == "value"):
                        self.map["_sourcePage"] = item[1]
                        break
            if ("name", "__fp") in attrs and "__fp" not in self.map:
                for item in attrs:
                    if (item[0] == "value"):
                        self.map["__fp"] = item[1]
                        break

    listname = ListName()
    listname.feed(html)

    # 准备登陆
    body = {
        "username": "823143047@qq.com",
        "password": "penguo1110",
        "login": "登陆",
        "hpts": hpts,
        "hptsh": hptsh,
        "showSwitchService": "true",
        "targetUrl": "/Home.action",
        "_sourcePage": listname.map["_sourcePage"],
        "__fp": listname.map["__fp"]
    }
    body = urllib.urlencode(body)
    headers["Content-Length"] = str(len(body))

    conn = httplib.HTTPSConnection("app.yinxiang.com")
    conn.request(method="POST", url="/Login.action", body=body, headers=headers)

    response = conn.getresponse()

    print(response.status)
    print(response.getheaders())
    # print(response.read())
    # html = response.read()

    result = []
    if response.status == 302:  # ok
        for item in response.getheader('set-cookie').split(';'):
            if 'JSESSIONID' in item or ('auth' in item and 'deleteme' not in item):
                result.append(item.split(',')[1])

    # print(html)

    conn.close()

    return result


def __commonHttp(url, body, contentType):
    headers = {
        "Host": "app.yinxiang.com",
        "Connection": "keep-alive",
        # "Content-Length": "551",
        "X-EN-Webclient-Version": "WEB2.0",
        "Origin": "https://app.yinxiang.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Content-Type": contentType,
        "X-GWT-Module-Base": "https://app.yinxiang.com/focusclient/",
        "X-GWT-Permutation": "258916150971A17BE80BC818F3CD7F22",
        "Accept": "*/*",
        "Referer": "https://app.yinxiang.com/Home.action",
        # "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6"
        # "Cookie": 'enAppInstalled=true; cookieTestValue=1447490094713; auth="S=s60:U=c44607:E=15105d0e5e7:C=1510599f84f:P=5fd:A=en-web:V=2:H=e45a07ae423766d6210befdf5aaa070a"; lastAuthentication=1447490095039/05c6de4de7d7a0f0d962a43f84baf6a5; JSESSIONID=091F9D2DDBD79BB6E94F84894B63BF49; _ga=GA1.2.614724134.1444233572; _gat=1; req_sec="U=c44607:P=/:E=15105349b70:S=aa1025cb69d21ee427361649cc337043"'
    }

    global __session_cookie

    headers["Cookie"] = __session_cookie[0] + "; " + __session_cookie[1]

    headers["Content-Length"] = str(len(body))

    conn = httplib.HTTPSConnection("app.yinxiang.com")
    conn.request(method="POST", url=url, body=body, headers=headers)

    response = conn.getresponse()

    ret = {"status": response.status, "headers": response.getheaders(), "content": response.read()}

    conn.close()

    return ret


def createPlainNote(title, content):
    """
    :param title: String 笔记标题
    :param content: String 笔记内容可以是html形式
    :return:None
    """

    noteBookId = '934f7d7f-ce9c-4c02-bf7c-3c91d4bcdf5e'  # PIS数据迁移 笔记本
    body = '7|0|15|https://app.yinxiang.com/focusclient/|6C220F57D140EFD49F2509CC748FB9B6|com.evernote.web.shared.GWTNoteStoreExtensions|createNote|com.evernote.edam.type.Note/4071998839|java.lang.String/2004016611|java.util.List|[Z/1413617015|com.evernote.edam.type.NoteAttributes/74627218|823143047||' + noteBookId + '|' + title + '|' + content + '|java.util.ArrayList/4159755760|1|2|3|4|3|5|6|7|5|8|6|0|1|1|0|1|0|1|9|8|12|0|0|0|0|0|0|0|0|0|0|0|1|0|0|10|0|0|0|0|0|0|0|0|0|0|A|A|A|A|0|0|0|0|A|11|0|0|VEFS5al|A|0|0|12|0|0|0|0|0|13|0|VEFS$df|14|15|0|'

    response = __commonHttp("/shard/s60/enweb/notestore/ext", body, "text/x-gwt-rpc; charset=UTF-8")

    print("createPlainNote status:%d" % response["status"])


def createFileNote(title, filepath):
    attachId = __uploadFile(filepath)

    body = '7|0|16|https://app.yinxiang.com/focusclient/|6C220F57D140EFD49F2509CC748FB9B6|com.evernote.web.shared.GWTNoteStoreExtensions|createNote|com.evernote.edam.type.Note/4071998839|java.lang.String/2004016611|java.util.List|[Z/1413617015|com.evernote.edam.type.NoteAttributes/74627218|823143047||934f7d7f-ce9c-4c02-bf7c-3c91d4bcdf5e|' + title + '|<div><br data-mce-bogus="1"></div>|java.util.ArrayList/4159755760|' + attachId + '|1|2|3|4|3|5|6|7|5|8|6|0|1|1|0|1|0|1|9|8|12|0|0|0|0|0|0|0|0|0|0|0|1|0|0|10|0|0|0|0|0|0|0|0|0|0|A|A|A|A|0|0|0|0|A|11|0|0|VEJFdW_|A|0|0|12|0|0|0|0|0|13|0|VEJF2lv|14|15|1|6|16|'

    print(body)
    response = __commonHttp("/shard/s60/enweb/notestore/ext", body, "text/x-gwt-rpc; charset=UTF-8")

    print("createImageNote status:%d" % response["status"])
    # print(response["headers"])
    # print(response["content"])


def get_mime_type(filename):  # filename 文件路径

    # 返回文件路径后缀名
    filename_type = os.path.splitext(filename)[1][1:]
    type_list = {
        'html': 'text/html',
        'htm': 'text/html',
        'shtml': 'text/html',
        'css': 'text/css',
        'xml': 'text/xml',
        'gif': 'image/gif',
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'js': 'application/x-javascript',
        'atom': 'application/atom+xml',
        'rss': 'application/rss+xml',
        'mml': 'text/mathml',
        'txt': 'text/plain',
        'jad': 'text/vnd.sun.j2me.app-descriptor',
        'wml': 'text/vnd.wap.wml',
        'htc': 'text/x-component',
        'png': 'image/png',
        'tif': 'image/tiff',
        'tiff': 'image/tiff',
        'wbmp': 'image/vnd.wap.wbmp',
        'ico': 'image/x-icon',
        'jng': 'image/x-jng',
        'bmp': 'image/x-ms-bmp',
        'svg': 'image/svg+xml',
        'svgz': 'image/svg+xml',
        'webp': 'image/webp',
        'jar': 'application/java-archive',
        'war': 'application/java-archive',
        'ear': 'application/java-archive',
        'hqx': 'application/mac-binhex40',
        'doc': 'application/msword',
        'pdf': 'application/pdf',
        'ps': 'application/postscript',
        'eps': 'application/postscript',
        'ai': 'application/postscript',
        'rtf': 'application/rtf',
        'xls': 'application/vnd.ms-excel',
        'ppt': 'application/vnd.ms-powerpoint',
        'wmlc': 'application/vnd.wap.wmlc',
        'kml': 'application/vnd.google-earth.kml+xml',
        'kmz': 'application/vnd.google-earth.kmz',
        '7z': 'application/x-7z-compressed',
        'cco': 'application/x-cocoa',
        'jardiff': 'application/x-java-archive-diff',
        'jnlp': 'application/x-java-jnlp-file',
        'run': 'application/x-makeself',
        'pl': 'application/x-perl',
        'pm': 'application/x-perl',
        'prc': 'application/x-pilot',
        'pdb': 'application/x-pilot',
        'rar': 'application/x-rar-compressed',
        'rpm': 'application/x-redhat-package-manager',
        'sea': 'application/x-sea',
        'swf': 'application/x-shockwave-flash',
        'sit': 'application/x-stuffit',
        'tcl': 'application/x-tcl',
        'tk': 'application/x-tcl',
        'der': 'application/x-x509-ca-cert',
        'pem': 'application/x-x509-ca-cert',
        'crt': 'application/x-x509-ca-cert',
        'xpi': 'application/x-xpinstall',
        'xhtml': 'application/xhtml+xml',
        'zip': 'application/zip',
        'bin': 'application/octet-stream',
        'exe': 'application/octet-stream',
        'dll': 'application/octet-stream',
        'deb': 'application/octet-stream',
        'dmg': 'application/octet-stream',
        'eot': 'application/octet-stream',
        'iso': 'application/octet-stream',
        'img': 'application/octet-stream',
        'msi': 'application/octet-stream',
        'msp': 'application/octet-stream',
        'msm': 'application/octet-stream',
        'mid': 'audio/midi',
        'midi': 'audio/midi',
        'kar': 'audio/midi',
        'mp3': 'audio/mpeg',
        'ogg': 'audio/ogg',
        'm4a': 'audio/x-m4a',
        'ra': 'audio/x-realaudio',
        '3gpp': 'video/3gpp',
        '3gp': 'video/3gpp',
        'mp4': 'video/mp4',
        'mpeg': 'video/mpeg',
        'mpg': 'video/mpeg',
        'mov': 'video/quicktime',
        'webm': 'video/webm',
        'flv': 'video/x-flv',
        'm4v': 'video/x-m4v',
        'mng': 'video/x-mng',
        'asx': 'video/x-ms-asf',
        'asf': 'video/x-ms-asf',
        'wmv': 'video/x-ms-wmv',
        'avi': 'video/x-msvideo'
    }
    # 判断数据中是否有该后缀名的 key
    if (filename_type in type_list.keys()):
        return type_list[filename_type]
    else:
        return 'application/octet-stream'


def __uploadFile(filepath):
    filename_type = os.path.splitext(filepath)[1][1:]
    mime_type = get_mime_type(filepath)

    newline = '\r\n'

    spliter = '------WebKitFormBoundaryAs0batMIQZgK4k7I' + newline
    name = 'Content-Disposition: form-data; name="file"; filename="default.' + filename_type + '"' + newline
    type = 'Content-Type: ' + mime_type + newline + newline
    content = open(filepath, "rb").read()
    end = '\r\n------WebKitFormBoundaryAs0batMIQZgK4k7I--' + newline

    body = bytes(spliter + name + type) + content + bytes(end)

    response = __commonHttp("/shard/s60/attach", body,
                            "multipart/form-data; boundary=----WebKitFormBoundaryAs0batMIQZgK4k7I")
    print(response["status"])
    xml = response["content"]
    print(xml)

    if response["status"] == 200:
        xml = urllib.unquote(xml)
        root = ElementTree.fromstring(xml)
        attachId = root.findall("attachment/id")[0].text
        print("attach id:" + attachId)
        return attachId


__session_cookie = __login()

# test
if __name__ == '__main__':
    createFileNote('图片笔记66666', '/Users/zhouzhipeng/Downloads/season_img_bigbanner_1_3.jpg')

    createPlainNote("abbbba",
                    '<div><br><img src="https://app.yinxiang.com/shard/s60/res/8b8cdff8-b0aa-4bd6-be9e-1d5bb036e0ce/season_img_bigbanner_1_1.jpg" alt="" name="8b8cdff8-b0aa-4bd6-be9e-1d5bb036e0ce" class="en-media" data-mce-src="https://app.yinxiang.com/shard/s60/res/8b8cdff8-b0aa-4bd6-be9e-1d5bb036e0ce/season_img_bigbanner_1_1.jpg"></div>')
