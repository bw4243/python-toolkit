#!/usr/bin/python
# -*-coding:utf-8-*-

import httplib
from moneydb import db
from moneydb.models import *
from moneydb.constants import *
from myutils import *
# db.add(CommonTask(user_id='3455', task_id='task22', task_name='taskname34', bundle_id='com.zhouzhipeng.dd'
#                   , process_name='ss', status=TASK_STATUS_WAIT, block_type=TASK_BLOCKED_TYPE_ONE
#                   , fire_time=nowtime_str(), type=TASK_TYPE_XIAO_BIN, extra='', add_time=nowtime_str(),
#                   update_time=nowtime_str()))


# print(db.session().query(CommonTask).filter_by(user_id='3455').one())

import userinfo
import taskrunner
from moneydb.constants import *

s = db.session()
# s.add(User(
#     user_id='16973020',
#     nick_name='',
#     cookie='Hm_lpvt_55a5855402d9f76f9739ffa75d37dfb2=1452391236; Hm_lvt_55a5855402d9f76f9739ffa75d37dfb2=1452334485,1452354788,1452355989,1452391203; OD=Olo0qpP2ElhpNGWckUiiypH4hQKMrRLKJJPAKQDG7giNe1A5gKj79A7LiAZtTPIK; JSESSIONID=BDEEB06418C807A76831269C923FE0B1; SERVERID=ec0dc4249f8af0df85b70311bff7ff5c|1452391297|1452388835',
#     app_type=APP_TYPE_XIAO_BIN,
#     idfa='5268855F-AA59-4BFE-B64F-61D04F19DE3C',
#     idfv='EE9251DE-E401-4340-BA4E-2A3171B1C480',
#     oid_md5='CBED9F24D48D24964B7B87BCD6AE8FF4',
#     uid='3c2e3d88ea4c7a407c08d5714bd13e3eaf0a3d74'
# ))



user = s.query(User).filter(User.user_id == '18538930').one()
# taskrunner.json_time('user_id=18538930&idfa=&bs=F5D439168VZFW5TBS&cc=130&app=1611445442,333206289,com.alipay.iphoneclient,474278250,0,143465,1,9.5.1%7c%7c1611445442,425349261,com.netease.news,474534964,0,143465,1,474%7c%7c(null),0,com.sogou.sogouinput,454115166,0,0,1,3.0.0')
# taskrunner.upload_process_status(user)

# finance = userinfo.get_user_finance(user)
# print(finance)

# taskrunner.applist(user)

# userinfo.log_download_xb(user)

# userinfo.sync_user_info(user)

# print(taskrunner.applist(user))

# userinfo.add_user()
# userinfo.bind_info(user)
#
# userinfo.sync_user_info(user)
# s.commit()
# s.close()


text = http_retry('http://xb.appshike.com/json_time', method='POST', body='p=LHn0y%2BBOAjuqSRcr%2BYVkOKbhPcPhRXasLujnCYIa1N1SPeEAqdXfT8wl6uZP8y2tbZl0QoLfI5e0OCpyKdMIm%2BQmqy08NbV32PDYn7YtpOhOlzRT4mWVIbv%2FKYAVxBF0wSl7Ngtph4zbPk%2FnsMtgBkwLGL9AEGEJe%2BAIXfZjSNc1yzpU9p%2F1qzzHCxWOq5VIv0DuTi2nMDR42DVJPOcpiQqJUsuMQY0kyLpb4hJdu8RwcwtSkKfWEK5pK7R%2BkpJ8VCNu13zgsR3vu5mxe5%2BhycDXpK0td7hdYINuMf6adDZD4%2BPoLuUJscx%2BeKQeN5GipuDJjNxY531HfXzj0UE%2FVfkEMC6P1cy7JJiNKRDahlkT8%2Flx92WJGvEu0hbjI7eb%2BX4GJF3obfhtoQZHC2ow6bMMMwYwrxZPJaWRrkYxKAGuMPg7vle4PDApJ7eLQKEGkTLI7JMZII42LhBG4bUjd3yUQQXuUacvhANp7se5%2FSfIHwwVUYnydKmHJ%2F1AWzXAgK8cW8LT%2FOIVIhzckd7WQg85Nr9uCwF1ikO3RXXEo4J%2FTKey69rezWpa7PotBjB5yHmZvGgMZRXuHr%2FcR%2BsXHZ0KZkNwgFr%2F%2Bx5uas5dVM%2BaHJ0aex612IWtI5C8pK6A1FY%2BLlqrzKdjx7mTZwhyj6cKtkEWYRG06L6jJybEOwsHVmTFHbJEukfl1r7Sns1YJmj4f%2BqqaZE5AJ3DEMInIMrF28q35R%2BuYgOKR8uJeJd0xAl1eyfmWeU06oGbV%2BFIFZzbbSKlbHVsfcyqT1hyQX%2Boibvo7d86ra7vudpcwOaivDa0H58KyHpFV0nfDT1hroJV3xaBjWyrjZOxUq7DZ2%2BqtGKGn7Y6mhq7VzIRWsVgQ%2BwLZje%2B4oJ8qM2pWXao%2FoNfAZDEFJKL9YYkDEVM8iZmp49WEfGcYzDYGSPu6xQcodNf5RRDL7T9wmTqpMlILdagf1lFjYbkHEruPjg0hH1VvOP0w%2BVKjKRq%2B3zgASVqfRdIuddaA%2BbOj1nt04pwudV5zFZAJujLDBeqG%2FS4HypZbFpWTAAZHS%2BGzg5GvOWSGe5idlwQAyKyRYT949rl', headers=headers_from_str("""
        Content-Type: application/x-www-form-urlencoded
        Connection: keep-alive
        Accept: */*
        User-Agent: com.gad.shiliu/1.19 CFNetwork/711.1.16 Darwin/14.0.0
        Accept-Language: zh-cn
    """))
logger.info(text.decode('utf-8'))





