from celery import Celery

# 设置django运行所依赖的环境变量
import os
project_name = os.path.split(os.path.abspath('.'))[-1]
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % project_name)

# 创建celery对象
celery_app = Celery('celery_tasks')
# 加载celery配置
celery_app.config_from_object('django.conf:settings')
# 让celery worker启动的时候自动发现有哪些任务函数
celery_app.autodiscover_tasks(['celery_tasks.raffles'])

