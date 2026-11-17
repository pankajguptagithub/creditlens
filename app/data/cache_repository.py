import json
import redis
from app.core.config import load_config
from redis.exceptions import RedisError, ConnectionError

def get_redis_client():
    config = load_config()

    return redis.Redis(
        host = config["redis"]["host"],
        port = config["redis"]["port"],
        decode_responses = True
    )
def get_cached_risk(customer_id):
    try:
        client = get_redis_client()

        cached_result = client.get(
            "risk:" + customer_id
        )

        if cached_result is None:
            return None

        return json.loads(cached_result)

    except (RedisError,ConnectionError):
        return None

def save_cached_risk(customer_id,risk_result):
    try:
        config = load_config()
        client = get_redis_client()

        client.setex(
            "risk:" + customer_id,
            config["redis"]["ttl_seconds"],
            json.dumps(risk_result)
        )
    except (RedisError,ConnectionError):
        return
