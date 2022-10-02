# -*- coding: utf-8 -*-
# @Time    : 9/29/22 10:04 PM
# @FileName: __init__.py.py
# @Software: PyCharm
# @Github    ：sudoskys

import redis
import time

_redis_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
_redis = redis.Redis(host='localhost', port=6379, decode_responses=True)


class JsonRedis(object):
    def __init__(self):
        """
        对 redis 进行直接操作
        """
        pass

    @staticmethod
    def create_data(user_id: str, group_id: str):
        """
        创建一个新的用户档案，使用当前时间值作为键名。
        :param user_id:
        :param group_id:

        :return: key ,data 返回dict仿api字段,只许str类型键
        """
        if not user_id:
            raise KeyError("not found user_id")
        if not group_id:
            raise KeyError("not found group_id")
        _time = str(int(time.time()))
        return time, {"user": str(user_id), "group": str(group_id)}

    def resign_user(self, userId: int, groupId: int):
        request_ = {"user_id": userId, "group_id": groupId}
        _key, _profile = self.create_data(**request_)
