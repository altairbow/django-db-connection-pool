# -*- coding: utf-8 -*-

from django.db.backends.mysql import base
from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin


class DatabaseWrapper(PooledDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(MySQLDialect_pymysql):
        server_version_info = (0, )

    def __str__(self):
        return 'MySQL connection to {HOST}/{NAME}'.format(**self.settings_dict)

    __repr__ = __str__
