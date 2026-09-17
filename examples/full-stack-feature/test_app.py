import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from app import RateLimiter

def test_initial_burst_allowed():
    limiter = RateLimiter(capacity=3, refill_rate_per_sec=1.0)
    client = "user_123"
    assert limiter.acquire(client) is True
    assert limiter.acquire(client) is True
    assert limiter.acquire(client) is True
    # 4th immediate request exceeds capacity
    assert limiter.acquire(client) is False

def test_token_replenishment():
    limiter = RateLimiter(capacity=2, refill_rate_per_sec=10.0) # 10 tokens/sec
    client = "user_456"
    assert limiter.acquire(client) is True
    assert limiter.acquire(client) is True
    assert limiter.acquire(client) is False
    
    time.sleep(0.15) # Wait for ~1.5 tokens
    assert limiter.acquire(client) is True

def test_invalid_cost_rejected():
    limiter = RateLimiter(capacity=5, refill_rate_per_sec=1.0)
    assert limiter.acquire("user_789", cost=0) is False
    assert limiter.acquire("user_789", cost=-2) is False
