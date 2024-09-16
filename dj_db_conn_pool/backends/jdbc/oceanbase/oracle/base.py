from django.db.backends.oracle import base
from sqlalchemy.dialects.oracle.base import OracleDialect

from dj_db_conn_pool.backends.jdbc.mixins import JdbcDialectMixin
from dj_db_conn_pool.backends.jdbc.oceanbase.mixins import JDBCOceanBaseDatabaseWrapperMixin


class DatabaseWrapper(JDBCOceanBaseDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(JdbcDialectMixin, OracleDialect):
        pass

    def init_connection_state(self):
        # TODO: custom OceanBase (Oracle mode) connection initialization
        pass
