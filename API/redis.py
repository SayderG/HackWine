import aioredis

redis = None


async def start_redis():
    global redis
    redis = await aioredis.from_url("redis://localhost:6379")


async def stop_redis():
    await redis.close()
