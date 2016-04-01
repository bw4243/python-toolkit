#!/usr/bin/python
# -*-coding:utf-8-*-

from scapy.all import *
from scapy.layers.inet import *


def run():
    USER_AGENTS = (  # items used for picking random HTTP User-Agent header value
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_0; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.678.0 Safari/534.21",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:0.9.2) Gecko/20020508 Netscape6/6.1",
        "Mozilla/5.0 (X11;U; Linux i686; en-GB; rv:1.9.1) Gecko/20090624 Ubuntu/9.04 (jaunty) Firefox/3.5",
        "Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10"
    )

    SOURCE = ['.'.join((str(random.randint(1, 254)) for _ in range(4))) for _ in range(100)]

    HTTPSTR = 'GET /shike?s=zhouzhipeng HTTP/1.0\r\nHost: %s\r\nUser-Agent: %s\r\n\r\n'

    domain = '127.0.0.1'
    http = HTTPSTR % (domain, random.choice(USER_AGENTS))
    sip=random.choice(SOURCE)
    print(sip)
    request = IP(src=sip, dst=domain) / TCP(dport=5000) / http
    resp=send(request)
    print(resp)

if __name__ == '__main__':
    run()
    #
    # result,unanswered=sr(IP(dst="www.baidu.com",ttl=(5,10))/ICMP())
    #
    # print(result)
    # print(unanswered)
