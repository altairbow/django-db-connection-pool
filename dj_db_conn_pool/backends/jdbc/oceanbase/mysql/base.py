# -*- coding: utf-8 -*-

import jpype
import jaydebeapi
from django.db.backends.mysql import base
from sqlalchemy.dialects.mysql.base import MySQLDialect
from dj_db_conn_pool.backends.jdbc.oceanbase.mixins import JDBCOceanBaseDatabaseWrapperMixin


class DatabaseWrapper(JDBCOceanBaseDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(MySQLDialect):
        def do_ping(self, dbapi_connection):
            try:
                return super(MySQLDialect, self).do_ping(dbapi_connection)
            except (jaydebeapi.DatabaseError, jpype.JException):
                return False

    def init_connection_state(self):
        # TODO: custom OceanBase (MySQL mode) connection initialization
        pass
