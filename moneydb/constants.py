#!/usr/bin/python
# -*-coding:utf-8-*-

# 任务执行状态
TASK_STATUS_WAIT = 'waiting'
TASK_STATUS_DOING = 'doing'
TASK_STATUS_COMPLETED = 'completed'
TASK_STATUS_TIMEOUT = 'timeout'

# 任务阻塞类型 比如:一个用户一次只能执行一个任务
BLOCKED_TYPE_ONE = 'one'
BLOCKED_TYPE_MULTIPLE = 'multiple'

# 任务类型,如小兵
APP_TYPE_XIAO_BIN = 'xiao_bin'
APP_TYPE_QIAN_KA = 'qian_ka'
