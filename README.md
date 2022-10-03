# BotRedis

一个 延迟队列实现

```python
import time
import asyncio
from QuickStar import JsonRedis

s = time.time()

# 初始化，如果没有则加载！
JsonRedis.start()

# 注册和通过
JsonRedis.resign_user(userId=1, groupId=-1)
JsonRedis.grant_resign(userId=1, groupId=-1)
JsonRedis.resign_user(userId=6, groupId=-1)


# 异步测试
async def main():
    from QuickStar import JsonRedis
    JsonRedis.resign_user(userId=3, groupId=-1)
    for i in range(20):
        JsonRedis.resign_user(userId=i + 1, groupId=-1)


asyncio.run(main())
JsonRedis.checker()  # check 传入的list中是一个值，带有 user 和group 的！可以通过子函数创建此值。也算是一个小漏洞？（可以改成深度遍历的哦）
e = time.time()
print(((e - s) * 1000), "毫秒")
```

基于内存共享和数据锁实现的原子化延迟队列

### 如何使用

自己改动 `QuickStar/__init__.py`