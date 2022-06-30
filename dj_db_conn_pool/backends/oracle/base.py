# -*- coding: utf-8 -*-

from django.db.backends.oracle import base
from cx_Oracle import DatabaseError
from sqlalchemy.dialects.oracle.base import OracleDialect
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin


class DatabaseWrapper(PooledDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(OracleDialect):
        def do_ping(self, dbapi_connection):
            try:
                return super(OracleDialect, self).do_ping(dbapi_connection)
            except DatabaseError:
                return False

    def _set_autocommit(self, autocommit):
        with self.wrap_database_errors:
            self.connection.connection.autocommit = autocommit
