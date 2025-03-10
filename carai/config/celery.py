# import os
# from celery import Celery

# # ✅ تحديد إعدادات Django لاستخدامها في Celery
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# app = Celery('config')

# # ✅ تحميل إعدادات Celery من `settings.py`
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # ✅ البحث عن التاسكات داخل كل التطبيقات
# app.autodiscover_tasks()
