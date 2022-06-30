# -*- coding: utf-8 -*-

from django.db.backends.mysql import base
from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin

import logging
logger = logging.getLogger(__name__)


class DatabaseWrapper(PooledDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(MySQLDialect_pymysql):
        server_version_info = (0, )

    def _set_autocommit(self, autocommit):
        with self.wrap_database_errors:
            try:
                self.connection.connection.autocommit(autocommit)
            except (Exception, ) as e:
                logger.exception('unable to set database(%s) autocommit: %s', self.alias, e)
