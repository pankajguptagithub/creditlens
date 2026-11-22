import json
import redis
import socket
from app.core.config import load_config
from redis.exceptions import RedisError, ConnectionError
from redis.backoff import NoBackoff
from redis.retry import Retry

def is_redis_available():
    config = load_config()

    if not config["redis"]["enabled"]:
        return false

    try:
        connection = socket.create_connection(
            (
                config["redis"]["host"],
                config["redis"]["port"],
            ),
            timeout=0.2
        )
        connection.close()

        return True

    except OSError:
        return False

def get_redis_client():
    config = load_config()

    return redis.Redis(
        host = config["redis"]["host"],
        port = config["redis"]["port"],
        decode_responses = True,
        socket_connect_timeout=0.2,
        socket_timeout=0.2,
        retry=Retry(NoBackoff(),0)
    )
def get_cached_risk(customer_id):

    #if not is_redis_available():
     #   return

    config = load_config()

    if not config["redis"]["enabled"]:
        return None, "BYPASS"

    try:
        client = get_redis_client()

        cached_result = client.get(
            "risk:" + customer_id
        )

        if cached_result is None:
            return None, "MISS"

        return json.loads(cached_result),"HIT"

    except (RedisError,ConnectionError):
        return None, "BYPASS"

def save_cached_risk(customer_id,risk_result):
    config = load_config()
    if not config["redis"]["enabled"]:
        return
    try:
        client = get_redis_client()

        client.setex(
            "risk:" + customer_id,
            config["redis"]["ttl_seconds"],
            json.dumps(risk_result)
        )
    except (RedisError,ConnectionError):
        return
