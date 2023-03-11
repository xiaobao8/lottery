from django.db import models
from utils.model import BaseModel
from utils.redis import RedisUtils
from raffle import utils


# Create your models here.

class PrizeModel(BaseModel):
    """
    奖品表
    """
    name = models.CharField(max_length=5, verbose_name="奖品名称")
    level = models.SmallIntegerField(verbose_name="奖的等级")
    num = models.IntegerField(verbose_name="数量")
    surplus_num = models.IntegerField(verbose_name="剩余数量", default=0)

    class Meta:
        db_table = "raffle_prize"
        verbose_name = "奖品表"


class WinningPrizeModel(BaseModel):
    """
    中奖奖品表
    """
    prize = models.ForeignKey(PrizeModel, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20, verbose_name="匿名用户ip识别")

    class Meta:
        db_table = "raffle_winningPrize"
        verbose_name = "中奖奖品表"

utils.save_cache()

