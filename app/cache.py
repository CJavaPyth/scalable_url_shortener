import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def cache_url(short_code: str, original_url: str, ttl: int = 3600):
    r.setex(short_code, ttl, original_url)


def get_cached_url(short_code: str):
    result = r.get(short_code)
    return result.decode() if result else None


def is_rate_limited(ip: str, limit: int = 5, period: int = 60) -> bool:
    key = f"rate:{ip}"
    current = r.get(key)
    if current and int(current) >= limit:
        return True
    else:
        p = r.pipeline()
        p.incr(key, 1)
        p.expire(key, period)
        p.execute()
        return False
