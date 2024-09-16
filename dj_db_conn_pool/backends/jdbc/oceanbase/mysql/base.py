from django.db.backends.mysql import base
from sqlalchemy.dialects.mysql.base import MySQLDialect

from dj_db_conn_pool.backends.jdbc.mixins import JDBCDialectMixin
from dj_db_conn_pool.backends.jdbc.oceanbase.mixins import JDBCOceanBaseDatabaseWrapperMixin


class DatabaseWrapper(JDBCOceanBaseDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(JDBCDialectMixin, MySQLDialect):
        pass
