import datetime
import logging

from django.db import models
from django.http import JsonResponse


# 统一返回信息代码
class ResultCode(models.TextChoices):
    DEFAULT = ('----', '默认值')
    SUCCESS = ('1000', '操作成功')

    # 公用服务错误码
    RAFFLE_FAIL = ('1001', '抽奖失败')

# 统一返回结果
class ResultJson:
    result = {
        'code': '',
        'msg': '',
        'description': '',
        'data': None,
        "time": ""
    }

    def __init__(self, ret=ResultCode.DEFAULT, code='1000', msg='操作成功', data=None, description='操作成功'):
        if ret is not ResultCode.DEFAULT:
            self.result['code'] = ret.value
            self.result['msg'] = ret.label
        else:
            self.result['code'] = code
            self.result['msg'] = msg
        self.result['data'] = data
        self.result['description'] = description
        self.result["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
