import logging

from django.db.backends.mysql import base
from sqlalchemy.dialects.mysql.base import MySQLDialect

from dj_db_conn_pool.core.mixins import PersistentDatabaseWrapperMixin

logger = logging.getLogger(__name__)


class DatabaseWrapper(PersistentDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(MySQLDialect):
        pass

    def _set_dbapi_autocommit(self, autocommit):
        self.connection.driver_connection.autocommit(autocommit)
