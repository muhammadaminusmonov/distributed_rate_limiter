import redis
import time


class FixedWindow:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def is_allowed(self, user_id: str, limit: int, window_seconds: int) -> bool:
        key = f"{user_id}:{time.time()//60}"
        count = self.redis.incr(key)
        if count == 1: self.redis.expire(key, window_seconds*2)
        print(self.redis.get(key))
        return count <= limit

r = redis.Redis(host='localhost', port=6379)
fixed_window = FixedWindow(r)
print(fixed_window.is_allowed("user1", 10, 120))