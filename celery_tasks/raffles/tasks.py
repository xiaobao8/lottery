# 封装celery任务函数
import json
from celery_tasks.main import celery_app
from utils.redis import RedisUtils
from django_celery_beat.models import CrontabSchedule, PeriodicTask, ClockedSchedule, PeriodicTasks, SolarSchedule, \
    IntervalSchedule
from raffle.models import WinningPrizeModel
from django.db import transaction
import datetime


@celery_app.task(name="add_tasks")
def add_tasks(task_name, run_func, one_off, run_type, run_param, args=[], kwargs={}, queue=None, enabled=1):
    """
    动态添加定时任务
    :param task_name:  定时任务名称
    :param run_func:   定时任务执行方法
    :param one_off:    是否执行一次
    :param run_type:   运行方式
    :param args:       参数
    :param kwargs:     关键字参数
    :param queue:      执行队列
    :return:
    """
    now = datetime.datetime.now()
    per_task = PeriodicTask(
        name=task_name, task=run_func, args=json.dumps(args), kwargs=json.dumps(kwargs), queue=queue, date_changed=now,
        one_off=one_off, enabled=enabled
    )
    if run_type == 'crontab':  # 周期任务 可配合one_off 执行一次
        default_param = {
            "minute": "*",
            "hour": "*",
            "day_of_week": "*",
            "day_of_month": "*",
            "month_of_year": "*",
            "timezone": "Asia/Shanghai",
        }
        default_param.update(**run_param)
        cron = CrontabSchedule(**default_param)
        cron.save()
        per_task.crontab = cron
    elif run_type == 'clocked':  # 指定时间执行
        """
        {
            clocked_time: ""
        }
        """
        clo = ClockedSchedule(**run_param)
        clo.save()
        per_task.clocked = clo
    else:
        return
    per_task.save()
    PeriodicTasks.changed(per_task)  # 刷新定时任务，如果不刷新则新设置的执行时间不会有效


def tasks_delete(task_name=None, kwargs=None):
    """
    删除定时任务  预防任务过多 导致数据运行延迟   根据任务名称和关键字参数做筛选
    :param task_name:  任务名称
    :param kwargs: 关键字参数的唯一值
    :return:
    """
    c_l = None
    if task_name:
        c_l = PeriodicTask.objects.filter(name=task_name)
    if kwargs:
        c_l = PeriodicTask.objects.filter(kwargs__contains=kwargs)
    if c_l:
        c = c_l.first()
        # ------------------- 删除定时任务执行器 --------------------
        crontab_id = c.crontab_id
        interval_id = c.interval_id
        solar_id = c.solar_id
        clocked_id = c.clocked_id
        if crontab_id:
            CrontabSchedule.objects.filter(id=crontab_id).delete()
        if interval_id:
            IntervalSchedule.objects.filter(id=interval_id).delete()
        if solar_id:
            SolarSchedule.objects.filter(id=solar_id).delete()
        if clocked_id:
            ClockedSchedule.objects.filter(id=clocked_id).delete()
        c_l.delete()


@celery_app.task(name="raffle_after")
def raffle_after(level, ip):
    # 存储记录
    key = "level_id_%s" % level
    level_id = RedisUtils.get(key)
    WinningPrizeModel.objects.create(prize_id=level_id, ip=ip)


