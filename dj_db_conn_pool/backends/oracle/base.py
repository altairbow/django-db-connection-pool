from django.db.backends.oracle import base
from sqlalchemy.dialects.oracle.base import OracleDialect

from dj_db_conn_pool.core.mixins import DatabasePoolWrapperMixin


class DatabaseWrapper(DatabasePoolWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(OracleDialect):
        pass

    def _set_dbapi_autocommit(self, autocommit):
        self.connection.driver_connection.autocommit = int(autocommit)
