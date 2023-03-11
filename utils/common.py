"""
公共函数
"""
import datetime
from functools import wraps
from lottery import settings
from rest_framework import status
from utils.Result import ResultJson, ResultCode
from rest_framework.response import Response

from hashlib import md5
import os
import uuid
import time


def get_uuid():
    """
    返回唯一的标识符
    :return:
    """
    return str(uuid.uuid1())


def response_data(ret=ResultCode.DEFAULT, code='1000', msg='操作成功', data=None, description='操作成功'):
    """
    数据返回函数
    :return:
    """
    result = ResultJson(ret=ret, code=code, msg=msg, data=data, description=description).result
    return Response(result)


def fail_response_data(ret=ResultCode.DEFAULT, code=ResultCode.RAFFLE_FAIL.value, msg=ResultCode.RAFFLE_FAIL.label,
                       data=None, description=""):
    """
    失败返回函数
    :return:
    """
    result = ResultJson(ret=ret, code=code, msg=msg, data=data, description=description).result
    return Response(result, status=status.HTTP_400_BAD_REQUEST)


# 获取客户端ip
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
