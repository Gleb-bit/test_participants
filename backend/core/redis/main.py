import json

from redis.asyncio import Redis as AsyncRedis


class RedisCache:
    def __init__(self, redis_client: AsyncRedis):
        self.redis_client = redis_client

    async def delete_cache(self, cache_key):
        await self.redis_client.delete(cache_key)

    async def get_cache(self, cache_key: str):
        cached_result = await self.redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

    async def set_cache(self, cache_key: str, value, expire_sec: int = 3600):
        await self.redis_client.set(cache_key, json.dumps(value), ex=expire_sec)
