# -*- coding: utf-8 -*-

from django.db.backends.oracle import base
from sqlalchemy.dialects.oracle.base import OracleDialect
from dj_db_conn_pool.backends.odbc.mixins import ODBCWrapperMixin
from dj_db_conn_pool.backends.odbc.utils import CursorWrapper


class DatabaseWrapper(ODBCWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(OracleDialect):
        pass

    def init_connection_state(self):
        pass

    def create_cursor(self, name=None):
        cursor = self.connection.cursor()
        return CursorWrapper(cursor)
