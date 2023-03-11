from configparser import ConfigParser, NoOptionError, NoSectionError
from django.conf import settings
import os.path


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = ConfigParser()
config.read(filenames=(os.path.join(BASE_DIR, 'config/config.ini')), encoding='utf-8')


def try_get(section, option, default=None):
    try:
        return config.get(section, option)
    except (NoSectionError, NoOptionError):
        return default


HOST_IP = try_get('server', 'ip')
DEBUG = try_get('server', 'debug')

DB_NAME = try_get("db", "name")
DB_USER = try_get("db", "user")
DB_PASS = try_get("db", "password")
DB_HOST = try_get("db", "host")
DB_PORT = try_get("db", "port")

REDIS_URL = try_get("redis", "url")
REDIS_PORT = try_get("redis", "port")
REDIS_PASSWORD = try_get("redis", "password")
REDIS_MAX_CONNECTIONS = try_get("redis", "max_connections")

PLAN = try_get("tactics", "plan")


#
# APP_ID = try_get("appid", "app_id")
#
# RABBITMQ_USER = try_get("rabbitmq", "username")
# RABBITMQ_PWD = try_get("rabbitmq", "password")
# RABBITMQ_HOST = try_get("rabbitmq", "host")
# RABBITMQ_PORT = try_get("rabbitmq", "port")
#
# YB_APP_KEY = try_get("yb", "app_key")
# YB_SECRET_KEY = try_get("yb", "secret_key")
# YB_URL = try_get("yb", "url")
# YB_VERSION = try_get("yb", "version")