from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from raffle import models, utils
from utils.redis import RedisUtils
from raffle.serializer import PrizeSerializer, WinningPrizeSerializer
from rest_framework import status
from celery_tasks.raffles import tasks
from utils import logger
from utils import common
from lottery import configuration
from django.db.models import F
import time
import random
import threading
from django.db import transaction


class RaffleAPIView(APIView):

    def post(self, *args, **kwargs):
        """
            抽奖api
            匿名用户：一个ip代表一个用户
            :param args:
            :param kwargs:
            :return:
        """
        ip = common.get_client_ip(self.request)  # 用户标识
        if configuration.PLAN == "1":
            # # 方案一  会有一定概率未抽中的情况  但效率高  利用django的查询修改原子操作保证不超发的情况。
            if RedisUtils.get("no_flag"):
                return common.fail_response_data(description="已抽完")
            # 一等奖数量
            level1 = RedisUtils.get("1")
            # 二等奖数量
            level2 = RedisUtils.get("2")
            # 三等奖数量
            level3 = RedisUtils.get("3")
            level_arr = [level1, level2, level3]
            if sum(level_arr) < 1:
                # 如果没数据了做标记
                RedisUtils.set("no_flag", 1)
                logger.info("已抽完")
                return common.fail_response_data(description="已抽完")
            # 按权重随机抽取
            level = random.choices(["1", "2", "3"], weights=level_arr)[0]
            ''
            # 数量-1
            if models.PrizeModel.objects.filter(level=level, surplus_num__gte=1).update(surplus_num=F("surplus_num") - 1):
                # 递减
                RedisUtils.decr(level)
                tasks.raffle_after.delay(level, ip)
                # key = "level_id_%s" % level
                # level_id = RedisUtils.get(key)
                # models.WinningPrizeModel.objects.create(prize_id=level_id, ip=ip)
            else:
                logger.info("未中奖")
                return common.fail_response_data(description="未中奖")
        else:
            # 方案二 保证100%中奖 但并发受限  因为考虑到100%中奖 所以使用悲观锁。
            s = RedisUtils.get("prize_sum")
            if s and s < 1:
                logger.info("已抽完")
                return common.fail_response_data(description="已抽完")
            if s is None:
                return common.fail_response_data(description="无奖品")
            try:
                with transaction.atomic():
                    pr_queryset = models.PrizeModel.objects.filter(surplus_num__gte=1).select_for_update()
                    if not len(pr_queryset):
                        logger.info("已抽完")
                        return common.fail_response_data(description="已抽完")
                    pr = random.choice(pr_queryset)
                    pr.surplus_num = pr.surplus_num - 1
                    pr.save()
                    RedisUtils.decr("prize_sum")
                models.WinningPrizeModel.objects.create(prize_id=RedisUtils.get("level_id_%s" % pr.level), ip=ip)
            except Exception as e:
                logger.error(e)

        return common.response_data()


class RaffleModelView(ModelViewSet):
    queryset = models.PrizeModel.objects.all()
    serializer_class = PrizeSerializer

    def destroy(self, request, *args, **kwargs):
        utils.save_cache()  # 数据缓存

        return super(RaffleModelView, self).destroy(request, *args, **kwargs)
