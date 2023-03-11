from raffle import models
from rest_framework.serializers import ModelSerializer
from utils.redis import RedisUtils
from lottery import configuration
from raffle import utils


class PrizeSerializer(ModelSerializer):

    class Meta:
        model = models.PrizeModel
        fields = ["name", "level", "num", "surplus_num", "id", "create_time"]
        read_only_fields = ("id", "create_time")

    def create(self, validated_data):
        resp = super(PrizeSerializer, self).create(validated_data)
        utils.save_cache()  # 数据缓存
        return resp

    def update(self, instance, validated_data):
        new_instance = super(PrizeSerializer, self).update(instance, validated_data)
        utils.save_cache()  # 数据缓存
        return new_instance


class WinningPrizeSerializer(ModelSerializer):

    class Meta:
        model = models.WinningPrizeModel
        fields = ["prize", "ip", "id", "create_time"]