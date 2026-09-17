import time
import threading
from typing import Dict, Tuple

class RateLimiter:
    def __init__(self, capacity: int = 5, refill_rate_per_sec: float = 2.0):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self._buckets: Dict[str, Tuple[float, float]] = {} # key -> (tokens, last_refill_timestamp)
        self._lock = threading.Lock()

    def acquire(self, client_id: str, cost: int = 1) -> bool:
        if cost <= 0:
            return False

        with self._lock:
            now = time.time()
            tokens, last_time = self._buckets.get(client_id, (float(self.capacity), now))
            
            # Replenish tokens
            elapsed = now - last_time
            tokens = min(float(self.capacity), tokens + elapsed * self.refill_rate)
            
            if tokens >= cost:
                tokens -= cost
                self._buckets[client_id] = (tokens, now)
                return True
            else:
                self._buckets[client_id] = (tokens, now)
                return False
