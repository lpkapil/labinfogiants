import pymysql
pymysql.install_as_MySQLdb()
# Include celery app in django project start.
from .celery import app

__all__ = ('app',) 