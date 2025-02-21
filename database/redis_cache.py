from redis.asyncio import Redis


redis = Redis(host='localhost', port=6379, db=1)


class Cache:
    @staticmethod
    async def set(user_id, data):
        await redis.set(name=user_id, value=data, ex=180)

    @staticmethod
    async def get(user_id):
        return await redis.get(user_id)

    @staticmethod
    async def clear(user_id):
        await redis.delete(user_id)
