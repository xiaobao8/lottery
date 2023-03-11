from django_redis import get_redis_connection
import logging

logger = logging.getLogger("log")
default_redis = get_redis_connection("default")
