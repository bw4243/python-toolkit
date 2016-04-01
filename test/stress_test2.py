#!/usr/bin python2.6
# -*- coding: utf-8 -*-


import threading, datetime, time
import logging
# close output that lower than error
from scapy.layers.inet import IP, TCP

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

# 初始最大并发数
START_THEAD_COUNT = 10

# 递增并发数
THREAD_INCREASE_STEP = 10

# 域名
DOMAIN = 'www.baidu.com'

# 默认http请求
METHOD = 'get'

# 请求发送间隔 整数
INTERVAL = 10  # 5秒

# 每个请求的超时
TIMEOUT = 5

SRC_IP = ['172.29.165.34',
          '172.29.165.35',
          '172.29.165.36',
          '172.29.165.37']

'''Factory'''
class biz :
    '''Main'''
    def run(self) :
        start = datetime.datetime.now()

        global FAILED_COUNT
        FAILED_COUNT = 0

        threads = []
        src_ip_upper_limit = len(SRC_IP) - 1
        
        # thread instance initialization
        for i in range(START_THEAD_COUNT) :
            src = SRC_IP[random.randint(0, src_ip_upper_limit)]
            t=threading.Thread(target=self.execute, args=(src, ))
            threads.append(t)

        # activate threads
        for i in range(START_THEAD_COUNT) :
            threads[i].start()

        # wait for all ends
        for i in range(START_THEAD_COUNT) :
            threads[i].join()

        delta = datetime.datetime.now() - start
        writeline('INFO', 'Totally \'' + str(START_THEAD_COUNT) + '\' http requests has been sent in ' + str(delta.seconds) + str(delta.microseconds / 1000) + 'ms.')
        # writeline('INFO', 'Total is \'' + str(START_THEAD_COUNT) + '\' while failed \'' + str(FAILED_COUNT) + '\' in ' + str(delta.seconds) + str(delta.microseconds / 1000) + 'ms.')
        return (True, None)


    '''Execute http request and get response status'''
    def execute(self, src) :

        global FAILED_COUNT
        
        sr(IP(dst = DOMAIN, src = src) / TCP(dport = 80), timeout = TIMEOUT, verbose = 0)
        # if unans : FAILED_COUNT = FAILED_COUNT + 1



'''Log writer'''
def writeline(status, msg) :
    line = time.strftime('%Y-%m-%d %X', time.localtime(time.time())) + ' [' + status + '] ' + msg
    print line
    return (True, line)


if __name__ == '__main__' :

    o = biz()

    while True :
        r, c = o.run()
        if not r : writeline('FAILED-', c)
        
        time.sleep(INTERVAL)
        
        # update max threads
        START_THEAD_COUNT = START_THEAD_COUNT + THREAD_INCREASE_STEP