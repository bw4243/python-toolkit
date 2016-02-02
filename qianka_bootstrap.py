#!/usr/bin/python
# -*-coding:utf-8-*-


# 1. setting the env
if __name__ == '__main__':
    import sys
    import os
    import time

    reload(sys)
    sys.setdefaultencoding("utf-8")

    current_path = os.path.split(os.path.realpath(__file__))[0]
    print(current_path)
    os.chdir(current_path)
    sys.path.insert(0, current_path)

    from qianka import taskrunner,userinfo

    # logic
    # for i in range(15):
    while 1:
        taskrunner.run(1)
        time.sleep(2)

    # refresh
    # userinfo.sync_user_status()
