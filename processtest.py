#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib
import os
import subprocess
from threading import Thread
import time


# class AsyncRunner(Thread):
#     def __init__(self, cmd, logfile):
#         self.cmd = cmd
#         self.logfile = logfile
#         Thread.__init__(self)
#     def run(self):
#         log = open(self.logfile, "w",0)
#
#         time.sleep(1)
#
#         subprocess.check_call(self.cmd, stdin=None, stdout=log, stderr=log, shell=True)
#
#         log.write("runner")
#         log.flush()
#         log.close()
#         # os.remove(self.logfile)
#
#
# log = open("/data/test.log",'w',0)
# log.write("test==============")
# # log.flush()
# print("before")
# # subprocess.check_call('sleep 2', stdin=None, stdout=log, stderr=log, shell=True,bufsize=0)
# AsyncRunner("echo 2\nsleep 3\necho 3","/data/test.log").start()
# print("after")
#
# # open(os.getenv("HOME").replaced("\\","/")+"/.bgpavim.trace",'w')
#


def deco(func):
    print("before method")
    func()
    print("after method")


def func():
    print("method func()")


# func = deco(func)
# func()

exec("print('sdfsd')")

import urllib

getattr()

