# -*- coding: utf-8 -*-
# @Time    : 9/29/22 10:04 PM
# @FileName: __init__.py.py
# @Software: PyCharm
# @Github    ：sudoskys
import json
import time

import redis
import uuid

_redis_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
_redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
_MsgTask = []


class JsonRedis(object):
    def __init__(self):
        """
        基于消息注册和操作器的实现。
        """
        # 如果没有消息，就尝试继承上次的消息队列
        global _MsgTask
        if _MsgTask:
            if Course := _redis.get("Telecha_Task"):
                _MsgTask = json.loads(Course)

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
        group_id = str(group_id)
        user_id = str(user_id)
        # 上版的时间戳导致了重复的几率，所以采用新的队列算法
        _time = str(int(time.time()))
        _uukey = uuid.uuid4()
        return f"tes_telecha_Task_{user_id}_{group_id}", {"user": str(user_id), "group": str(group_id),
                                                          "time": _time}

    @staticmethod
    def getAllTask():
        return _redis.scan_iter("tes_telecha_Task_*")

    def resign_user(self, userId: int, groupId: int):
        request_ = {"user_id": userId, "group_id": groupId}
        _key, _profile = self.create_data(**request_)
        _redis.set(_key, json.dumps(_profile))

    def grant_resign(self, userId: int, groupId: int):
        request_ = {"user_id": userId, "group_id": groupId}
        _key, _ = self.create_data(**request_)
        if _redis.delete(_key):
            return _key
        else:
            return "没有记录"

    def remove_user(self):
        pass
