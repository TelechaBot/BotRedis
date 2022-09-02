from Bot import TimerRedis

TimerRedis.JsonRedis.resign_user(userId=100, groupId=100)

TimerRedis.JsonRedis.grant_resign(userId=100, groupId=100)

print("因为架构变动，所以部分方法使用了异步，你也可以在仓库历史或者同步分支中找到同步版本，核心就是Checker")


"""
你可以调用checker来实现过期操作

如果是同步，可以使用自带的定时器（Timer库）需要自行改动
如果是异步，请看下面的注释
"""

"""
import aioschedule
aioschedule.every(3).seconds.do(JsonRedis.checker)

async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(bot.polling(otherFunc(), scheduler())
asyncio.run(main())
"""
