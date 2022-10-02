# -*- coding: utf-8 -*-
# @Time    : 9/29/22 10:04 PM
# @FileName: __init__.py.py
# @Software: PyCharm
# @Github    ：sudoskys
import json
import time
import redis
import uuid
import multiprocessing

task_lock = multiprocessing.Lock()
_redis_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
_redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
_MsgTask = {}


class JsonRedis(object):

    @staticmethod
    def start():
        """
        全内存队列设计，操作全局变量的同时做到中断重载
        优化在于深度遍历
        """
        # 如果没有消息，就尝试继承上次的消息队列
        global _MsgTask, task_lock
        try:
            task_lock.acquire()
            if len(_MsgTask) == 0:
                if Course := _redis.get("Telecha_Task"):
                    _MsgTask = json.loads(Course)
                    print("队列:初始化上次检查的数据")
        except Exception as err:
            raise err
        finally:
            task_lock.release()

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
        return f"Task_{user_id}_{group_id}", {"user": user_id,
                                              "group": group_id,
                                              "time": _time,
                                              "uuid": str(_uukey),
                                              "interval": 10,
                                              }

    @staticmethod
    def resign_user(userId: int, groupId: int):
        global _MsgTask, task_lock
        try:
            task_lock.acquire()
            request_ = {"user_id": userId, "group_id": groupId}
            _key, _profile = JsonRedis.create_data(**request_)
            if not _MsgTask.get(_key):
                _MsgTask[_key] = _profile
            else:
                pass
        except Exception as err:
            raise err
        finally:
            task_lock.release()

    @staticmethod
    def grant_resign(userId: int, groupId: int):
        request_ = {"user_id": userId, "group_id": groupId}
        _key, _ = JsonRedis.create_data(**request_)
        if Data := _MsgTask.get(_key):
            JsonRedis.checker(unban=[_key])
            return Data.get("uuid")
        else:
            return "没有记录"

    @staticmethod
    def remove_user(userId: int, groupId: int):
        request_ = {"user_id": userId, "group_id": groupId}
        _key, _ = JsonRedis.create_data(**request_)
        JsonRedis.checker(dismiss=[_key])

    @staticmethod
    def checker(ban=None, unban=None, dismiss=None):
        global _MsgTask, task_lock
        if dismiss is None:
            dismiss = []
        if unban is None:
            unban = []
        if ban is None:
            ban = []
        # 先处理掉 dismiss 的数据，然后对数据进行检查，添加到执行队列封杀
        try:
            task_lock.acquire()
            # 数据释放与处理
            for key in dismiss:
                _MsgTask.pop(key, None)
            for key in unban:
                _MsgTask.pop(key, None)
            # 过期检查
            for key in _MsgTask:
                _data = _MsgTask[key]
                if abs(int(time.time()) - int(_data["time"])) > int(_data["interval"]):
                    ban.append(key)
            for key in ban:
                profile = _MsgTask[key]
                userId = profile.get("user")
                groupId = profile.get("group")
                uuid = profile.get("uuid")
                print(f"释放{uuid}，{userId}-{groupId}")
                _MsgTask.pop(key, None)
            # 存储队列数据
            _redis.set("Telecha_Task", json.dumps(_MsgTask))
        except Exception as err:
            raise err
        finally:
            task_lock.release()
