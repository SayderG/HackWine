import aioredis

redis = None


async def get_redis():
    global redis
    if redis is None:
        redis = await aioredis.from_url("redis://localhost:6379")
    return redis


async def stop_redis():
    global redis
    if redis is not None:
        await redis.close()
        await redis.wait_closed()
        redis = None
