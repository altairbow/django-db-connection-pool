from django.db.backends.oracle import base
from sqlalchemy.dialects.oracle.base import OracleDialect

from dj_db_conn_pool.backends.odbc.mixins import ODBCDatabaseWrapperMixin


class DatabaseWrapper(ODBCDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(OracleDialect):
        pass

    def init_connection_state(self):
        pass
