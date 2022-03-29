# -*- coding: utf-8 -*-

from django.db.backends.oracle import base
from cx_Oracle import DatabaseError
from sqlalchemy.dialects.oracle.cx_oracle import OracleDialect
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin


class DatabaseWrapper(PooledDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(OracleDialect):
        def do_ping(self, dbapi_connection):
            try:
                return super(OracleDialect, self).do_ping(dbapi_connection)
            except DatabaseError:
                return False

    def __str__(self):
        return 'Oracle connection to {NAME}'.format(**self.settings_dict)

    __repr__ = __str__
