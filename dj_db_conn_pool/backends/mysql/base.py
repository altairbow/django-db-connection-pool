# -*- coding: utf-8 -*-

from django.db.backends.mysql import base
from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin

import logging
logger = logging.getLogger(__name__)


class DatabaseWrapper(PooledDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(MySQLDialect_pymysql):
        pass

    def _set_dbapi_autocommit(self, autocommit):
        self.connection.connection.autocommit(autocommit)
