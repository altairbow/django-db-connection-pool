from django.db.backends.oracle import base
from cx_Oracle import DatabaseError
from sqlalchemy.dialects.oracle.cx_oracle import OracleDialect
from dj_db_conn_pool.backends import BaseDatabaseWrapper


class Dialect(OracleDialect):
    def do_ping(self, dbapi_connection):
        try:
            return super().do_ping(dbapi_connection)
        except DatabaseError:
            return False


class DatabaseWrapper(BaseDatabaseWrapper, base.DatabaseWrapper):
    SQLAlchemyDialect = Dialect
