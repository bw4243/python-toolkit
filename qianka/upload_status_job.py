#!/usr/bin/python
# -*-coding:utf-8-*-


import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from db import disciple
import taskrunner
import time
import userinfo

if __name__ == '__main__':
    while 1:
        for data in disciple.fetch_will_complete():
            taskrunner.upload_app_status(data)
            data['has_uncompleted'] = 0
            data['now_task'] =data['now_task'].encode('unicode-escape')
            disciple.update_task_info(data)

        time.sleep(1)