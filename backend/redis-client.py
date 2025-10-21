import redis
import os
from dotenv import load_dotenv


redis_client = redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379"),
    decode_responses=True
)

## Function checks if the short_code exists in the Redis cache
## decode_responses allows us to return strings instead of bytes

def get_cached_url(short_code: str):
    return redis_client.get(f"${short_code}")

## Function to cache the url
## we use setex instead of set because setex stores data with an expiration
# time and in this case, we set it to 86400 seconds which is equivalent to 24 hours 
def cache_url(short_code: str, original_url: str, expiry=86400):
    redis_client.setex(f"url ${short_code}", expiry, original_url)
