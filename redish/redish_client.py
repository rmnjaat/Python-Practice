import redis

class RedisClient:
    _instance = None

    def __new__(cls, host, port):
        if cls._instance is None:
            cls._instance = redis.Redis(host=host, port=port, decode_responses=True)
        return cls._instance

