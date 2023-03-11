from django.db import models
from django.conf import settings
import re


class MetaBase(type):

    def __init__(self, name, bases, dic):
        super().__init__(name, bases, dic)
        table_name = re.findall(r"[^.]+", self.__qualname__)[0].replace("Models", "")
        self.db_table = "{prefix}_{name}".format(prefix=settings.DATA_TABLE_PREFIX, name=table_name)


class BaseModel(models.Model):
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True