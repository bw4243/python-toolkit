#!/usr/bin/python
# -*-coding:utf-8-*-

# 可选参数: python run_task_job.py xiao_bin
# 参数分别含义为: 类型

import sys
import os

import time


def init():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    current_path = os.path.split(os.path.realpath(__file__))[0]
    print(current_path)
    os.chdir(current_path[:current_path.rfind('/')])
    sys.path.insert(0, current_path[:current_path.rfind('/')])


def run():
    from moneydb.constants import APP_TYPE_XIAO_BIN
    from moneydb.models import User, Task
    from myutils import logger

    args = sys.argv

    try:
        if len(args) != 2:
            logger.error('At least 1 params when startup the job!!!!')
            return

        app_type = args[1]

        # 根据app_type 导入不同的app模块
        runner = None
        if app_type == APP_TYPE_XIAO_BIN:
            from shike import taskrunner as runner

            # init_log('/data/logs/shike/shike.log')
        # TODO:其他类别的app


        # 简单处理,每隔15s检查一次
        end_time = start_time = int(time.time())
        while (end_time - start_time) < 55:
            end_time = int(time.time())
            # 1. 抓取指定数量的Task
            tasks = Task.fetch_waiting_tasks(app_type)

            logger.info('run_task_job tasks:')
            logger.info(tasks)

            for task in tasks:
                # 2.根据user_id找到user
                user = User.get(task.user_id)
                # 3.开启线程执行任务
                runner.run_task(user, task)

            time.sleep(5)
        logger.info('run_task_job[%s] speeds time: %ds' % (args[1], (end_time - start_time)))
    except:
        logger.exception('run_task_job[%s]  errors!' % args[1])


if __name__ == '__main__':
    init()
    run()
