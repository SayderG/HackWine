import aioredis

redis = None


async def start_redis():
    global redis
    redis = await aioredis.from_url("redis://localhost")


async def stop_redis():
    redis.close()
    await redis.wait_closed()
