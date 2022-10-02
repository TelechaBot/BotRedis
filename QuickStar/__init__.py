# -*- coding: utf-8 -*-
# @Time    : 9/29/22 10:04 PM
# @FileName: __init__.py.py
# @Software: PyCharm
# @Github    ：sudoskys

import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


class JsonRedis(object):
    @staticmethod
    def init_data():
        if not globals().get("__quick_task"):
            task = r.get('telecha_tasks')
            if task is not None:
                globals()["__quick_task"] = task
            else:
                globals()["__quick_task"] = {}

    def resign(self):
        self.init_data()
        print(globals()["__quick_task"])
