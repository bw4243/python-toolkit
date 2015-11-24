#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename: paxel.py
# FROM: http://fayaa.com/code/view/58/full/
# Jay modified it a little and save for further potential usage.

'''It is a multi-thread downloading tool

    It was developed following axel.
        Author: volans
        E-mail: volansw [at] gmail.com
'''

import sys
import os
import time
import urllib
from threading import Thread, Lock
import shutil
from contextlib import closing

printLocker = Lock()

# in case you want to use http_proxy
local_proxies = {'http': 'http://131.139.58.200:8080'}


class AxelPython(Thread, urllib.FancyURLopener):
    '''Multi-thread downloading class.

        run() is a vitural method of Thread.
    '''

    def __init__(self, threadname, url, filename, ranges, proxies={}):
        Thread.__init__(self, name=threadname)
        urllib.FancyURLopener.__init__(self, proxies)
        self.name = threadname
        self.url = url
        self.filename = filename
        self.ranges = ranges
        self.downloaded = 0

    def run(self):
        '''vertual function in Thread'''
        try:
            self.downloaded = os.path.getsize(self.filename)
        except OSError:
            # print 'never downloaded'
            self.downloaded = 0

        # rebuild start poind
        self.startpoint = self.ranges[0] + self.downloaded

        # This part is completed
        if self.startpoint >= self.ranges[1]:
            print 'Part %s has been downloaded over.' % self.filename
            return

        self.oneTimeSize = 16384  # 16kByte/time
        printLocker.acquire()
        print 'task %s will download from %d to %d' % (self.name, self.startpoint, self.ranges[1])
        printLocker.release()

        self.addheader("Range", "bytes=%d-%d" % (self.startpoint, self.ranges[1]))
        self.urlhandle = self.open(self.url)

        data = self.urlhandle.read(self.oneTimeSize)
        while data:
            filehandle = open(self.filename, 'ab+')
            filehandle.write(data)
            filehandle.close()

            self.downloaded += len(data)
            # print "%s" % (self.name)
            # progress = u'\r...'

            data = self.urlhandle.read(self.oneTimeSize)


def GetUrlFileSize(url, proxies={}):
    with closing(urllib.urlopen(url, proxies=proxies)) as urlHandler:
        length = urlHandler.headers.getheader('Content-Length')
        if length is None:
            return 0
        else:
            return int(length)


def SpliteBlocks(totalsize, blocknumber):
    blocksize = totalsize / blocknumber
    ranges = []
    for i in range(0, blocknumber - 1):
        ranges.append((i * blocksize, i * blocksize + blocksize - 1))
    ranges.append((blocksize * (blocknumber - 1), totalsize - 1))

    return ranges


def islive(tasks):
    for task in tasks:
        if task.isAlive():
            return True
    return False


def paxel(url, output, blocks=6, proxies=local_proxies):
    ''' paxel
    '''
    size = GetUrlFileSize(url, proxies)
    ranges = SpliteBlocks(size, blocks)

    threadname = ["thread_%d" % i for i in range(0, blocks)]
    filename = ["tmpfile_%d" % i for i in range(0, blocks)]

    tasks = []
    for i in range(0, blocks):
        task = AxelPython(threadname[i], url, filename[i], ranges[i])
        task.setDaemon(True)
        task.start()
        tasks.append(task)

    time.sleep(2)

    lastDownloaded = 0
    # speed=0
    while islive(tasks):
        downloaded = sum([task.downloaded for task in tasks])
        speed = (downloaded - lastDownloaded) * 2 / 1024

        process = downloaded / float(size) * 100
        show = u'\rFilesize:%dM Downloaded:%dM Completed:%.2f%% Speed:%dkb/s' % (
        size / 1024 / 1024, downloaded / 1024 / 1024, process, speed)
        sys.stdout.write(show)
        sys.stdout.flush()
        time.sleep(0.5)

        lastDownloaded = downloaded

    sys.stdout.write(u'\rFilesize:{0} Downloaded:{0} Completed:100%  \n'.format(size))
    sys.stdout.flush()

    with open(output, 'wb+') as filehandle:
        for i in filename:
            with open(i, 'rb') as f:
                shutil.copyfileobj(f, filehandle, 102400)
            try:
                os.remove(i)
            except OSError:
                pass


if __name__ == '__main__':
    url = 'http://dldir1.qq.com/qqfile/QQforMac/QQ_V3.1.1.dmg'
    url = 'http://lx.cdn.baidupcs.com/file/d779a23db6566666fe6ef83a19f56654?bkt=p3-1400d779a23db6566666fe6ef83a19f5665412e4f369000019717a97&xcode=43a37d0c5114ca8dc6318f1f598acfbd7bf65c26a40e2768ea3971ac1f4f1a6a&fid=3289602521-250528-1042517148186690&time=1448205743&sign=FDTAXGERLBH-DCb740ccc5511e5e8fedcff06b081203-qBmZAril3zpaSUX4FVhBwh%2BZsbg%3D&to=cb&fm=Nan,B,G,bs&sta_dx=407&sta_cs=6&sta_ft=dmg&sta_ct=0&fm2=Nanjing02,B,G,bs&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=1400d779a23db6566666fe6ef83a19f5665412e4f369000019717a97&sl=71696462&expires=8h&rt=pr&r=471878881&mlogid=7560254590878295089&vuk=3289602521&vbdid=1010685645&fin=ideaIU-15.0.1-custom-jdk-bundled.dmg&fn=ideaIU-15.0.1-custom-jdk-bundled.dmg&slt=pm&uta=0&rtype=1&iv=0&isw=0&dp-logid=7560254590878295089&dp-callid=0.1.1'
    # dowloading this master.zip file is a bug
    # url = 'https://github.com/openstack/nova/archive/master.zip'
    output = 'download.file'
    paxel(url, output, blocks=10, proxies={})
