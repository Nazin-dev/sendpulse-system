import redis

redis_client = redis.Redis(
    host='localhost',  # ou 'localhost'
    port=6379,
    db=0,
)
