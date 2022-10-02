# -*- coding: utf-8 -*-
# @Time    : 10/1/22 3:26 PM
# @FileName: task.py
# @Software: PyCharm
# @Github    ：sudoskys
import asyncio
import time

from QuickStar import JsonRedis

s = time.time()

JsonRedis.start()

JsonRedis.resign_user(userId=1, groupId=-1)
JsonRedis.grant_resign(userId=1, groupId=-1)
JsonRedis.resign_user(userId=6, groupId=-1)


async def main():
    from QuickStar import JsonRedis
    JsonRedis.resign_user(userId=3, groupId=-1)
    for i in range(20):
        JsonRedis.resign_user(userId=i + 1, groupId=-1)


asyncio.run(main())
JsonRedis.resign_user(userId=2, groupId=-1)
JsonRedis.checker()

e = time.time()
print(((e - s) * 1000), "毫秒")
