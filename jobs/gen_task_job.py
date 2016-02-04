#!/usr/bin/python
# -*-coding:utf-8-*-

# 可选参数: python gen_task_job.py 16973020
# 参数分别含义为: user_id

import sys
import os
import time


def init():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    current_path = os.path.split(os.path.realpath(__file__))[0]
    print(current_path)
    os.chdir(current_path)
    sys.path.insert(0, current_path)


def run():
    from moneydb.constants import APP_TYPE_XIAO_BIN
    from moneydb.models import User
    from myutils import logger

    args = sys.argv
    try:

        if len(args) != 2:
            logger.error('At least 1 params when startup the job!!!!')
            return

        user = User.fetch_valid_one(args[1])
        logger.info(user)
        if not user:
            logger.info('user[%s] is busy! just skip over' % args[1])
            return

        app_type = user.app_type

        # 根据app_type 导入不同的app模块
        runner = None
        if app_type == APP_TYPE_XIAO_BIN:
            from shike import taskrunner as runner

            # init_log('/data/logs/shike/shike.log')
            # from myutils import logger
        # TODO:其他类别的app





        # 因为linux的crontab只能一分钟执行一次,故需要多次循环执行以提高效率
        end_time = start_time = int(time.time())
        while (end_time - start_time) < 55:
            end_time = int(time.time())
            user = User.fetch_valid_one(args[1])
            if not user: break
            # 生成任务
            runner.gen_task(user)
            time.sleep(2)

        logger.info('gen_task_job[%s] speeds time: %ds' % (args[1], (end_time - start_time)))
    except:
        logger.exception('gen_task_job[%s]  errors!' % args[1])


if __name__ == '__main__':
    init()
    run()
