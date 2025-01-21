# lcim/celery_config.py

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Set redis broker_connection_retry_on_startup within the CELERY namespace
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'app_wp_plugin_server_populate_plugin_versions': {
        'task': 'app_wp_plugin_server.tasks.populate_plugin_versions',
        'schedule': 5.0,  # Every 5 seconds
    },
    # 'app_imp_mywork_process': {
    #     'task': 'app_imp_clearance.tasks.process_mywork_queue',
    #     'schedule': 5.0,  # Every 5 seconds
    # },
    # 'app_imp_clearance-docs-delete': {
    #     'task': 'app_imp_clearance.tasks.schedule_mywork_jobs_docs_delete',
    #     'schedule': crontab(minute='*/5'),  # Every 5 minutes
    # },
    # 'auapp_logging_process_logs': {
    #     'task': 'dhl_common_package.auapp_logging.tasks.process_logs',
    #     'schedule': crontab(minute='*/1'),  # Every 1 minute
    # },
    # 'auapp_logging_delete_old_logs': {
    #     'task': 'dhl_common_package.auapp_logging.tasks.delete_old_logs',
    #     'schedule': crontab(minute=0, hour=21),  # Every day at 9:00 PM
    #     'kwargs': {'days': 7}  # delete logs older than 7 days from db
    # },
    # 'app_user_management_deactivation_reminder': {
    #     'task': 'dhl_common_package.app_user_management.tasks.deactivation_reminder',
    #     'schedule': crontab(minute=0, hour=9),  # Every day at 9:00 AM
    #     'kwargs': {
    #         'no_of_days': settings.APP_USER_MANAGEMENT_CRON_DEACTIVATION_REMINDER_DAYS,
    #         'verbose': True
    #     }
    # },
    # 'app_user_management_deactivate_users': {
    #     'task': 'dhl_common_package.app_user_management.tasks.deactivate_users',
    #     'schedule': crontab(minute=30, hour=9),  # Every day at 9:30 AM
    #     'kwargs': {
    #         'no_of_days': settings.APP_USER_MANAGEMENT_CRON_DEACTIVATION_REMINDER_DAYS,
    #         'grace_period_days': settings.APP_USER_MANAGEMENT_CRON_USER_DEATIVATION_GRACE_PERIOD_DAYS,
    #         'verbose': True
    #     }
    # },
    # 'app_user_management_delete_users': {
    #     'task': 'dhl_common_package.app_user_management.tasks.delete_users',
    #     'schedule': crontab(minute=0, hour=10),  # Every day at 10:00 AM
    #     'kwargs': {
    #         'no_of_days': settings.APP_USER_MANAGEMENT_CRON_DEACTIVATION_REMINDER_DAYS,
    #         'grace_period_days': settings.APP_USER_MANAGEMENT_CRON_USER_DEATIVATION_GRACE_PERIOD_DAYS,
    #         'delete_after_days': settings.APP_USER_MANAGEMENT_CRON_DELETE_USERS_DAYS,
    #         'verbose': True
    #     }
    # },
}

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
