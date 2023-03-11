from raffle import models
from utils.redis import RedisUtils
from lottery import configuration


# 方案一缓存
def plan_1_cache():
    p = models.PrizeModel.objects.values("level", "num", "id")
    for i in p:
        RedisUtils.set(i["level"], i["num"])
        RedisUtils.set("level_id_%s" % i["level"], i["id"])

# 方案二缓存
def plan_2_cache():
    sum_ = sum(list(models.PrizeModel.objects.values_list("surplus_num", flat=True)))
    RedisUtils.set("prize_sum", sum_)


def save_cache():
    if configuration.PLAN == "1":
        # 方案一的缓存
        plan_1_cache()
    else:
        # 方案二缓存
        plan_2_cache()