import redis
import time
import uuid

class SlydingWindow:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def is_allowed(self, user_id: str, limit: int, window_seconds: int):
        key = f"{user_id}"
        now = time.time()
        window_start = now - window_seconds
        member = f"{uuid.uuid4()}"

        self.redis.zremrangebyscore(key, '-inf', window_start)
        count = self.redis.zcard(key)
        if count >= limit: return False
        self.redis.zadd(key, {member: now})
        self.redis.expire(key, window_seconds)
        return True

r = redis.Redis(host='localhost', port=6379)
slyding_window = SlydingWindow(r)
print(slyding_window.is_allowed("user1", 10, 120))