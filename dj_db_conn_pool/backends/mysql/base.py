from django.db.backends.mysql import base
from sqlalchemy.dialects.mysql.base import MySQLDialect
from dj_db_conn_pool.backends import BaseDatabaseWrapper


class Dialect(MySQLDialect):
    def _extract_error_code(self, exception):
        return exception.args[0]


class DatabaseWrapper(BaseDatabaseWrapper, base.DatabaseWrapper):
    SQLAlchemyDialect = Dialect
