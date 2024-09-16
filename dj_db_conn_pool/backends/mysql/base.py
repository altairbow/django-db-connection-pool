import logging

from django.db.backends.mysql import base
from sqlalchemy.dialects.mysql.mysqldb import MySQLDialect_mysqldb as MySQLDialect

from dj_db_conn_pool.core.mixins import DatabasePoolWrapperMixin

logger = logging.getLogger(__name__)


class DatabaseWrapper(DatabasePoolWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(MySQLDialect):
        pass

    def _set_dbapi_autocommit(self, autocommit):
        self.connection.driver_connection.autocommit(autocommit)
