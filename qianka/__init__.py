#!/usr/bin/python
# -*-coding:utf-8-*-

import os
import sys

print('init')

# 1. setting the env
reload(sys)
sys.setdefaultencoding("utf-8")

current_path = os.path.split(os.path.realpath(__file__))[0]
print(current_path)
os.chdir(current_path)
# sys.path.insert(0, module_path)


