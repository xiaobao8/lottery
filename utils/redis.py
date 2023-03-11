from utils import default_redis
import json


class RedisUtils:

    @staticmethod
    def set(key, value, expires=None):
        """
        存储数据
        :param key:
        :param value:
        :param expires:
        :return:
        """
        if expires:
            default_redis.set(key, json.dumps(value), int(expires))
        else:
            default_redis.set(key, json.dumps(value))

    @staticmethod
    def get(key):
        """
        根据key获取数据
        :param key:
        :return:
        """
        value = default_redis.get(key)
        if value:
            return json.loads(value)
        return value

    @staticmethod
    def delete(*key):
        """
        删除key
        :param key:
        :return:
        """
        default_redis.delete(*key)

    @staticmethod
    def decr(key):
        default_redis.decr(key)