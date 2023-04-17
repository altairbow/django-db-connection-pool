# -*- coding: utf-8 -*-

import jpype.dbapi2
from django.db.backends.oracle import base
from sqlalchemy.dialects.oracle.base import OracleDialect
from dj_db_conn_pool.backends.jdbc.oceanbase.mixins import JDBCOceanBaseDatabaseWrapperMixin


class DatabaseWrapper(JDBCOceanBaseDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(OracleDialect):
        def do_ping(self, dbapi_connection):
            try:
                return super(OracleDialect, self).do_ping(dbapi_connection)
            except jpype.dbapi2.DatabaseError:
                return False

    def init_connection_state(self):
        # TODO: custom OceanBase (Oracle mode) connection initialization
        pass
