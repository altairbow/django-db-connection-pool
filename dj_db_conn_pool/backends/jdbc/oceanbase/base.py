# -*- coding: utf-8 -*-

import jpype
import jaydebeapi
from django.db.backends.oracle import base
from sqlalchemy.dialects.oracle.base import OracleDialect
from dj_db_conn_pool.backends.jdbc import JDBCDatabaseWrapper


import logging
logger = logging.getLogger(__name__)


class DatabaseWrapper(JDBCDatabaseWrapper, base.DatabaseWrapper):
    class SQLAlchemyDialect(OracleDialect):
        def do_ping(self, dbapi_connection):
            try:
                return super(OracleDialect, self).do_ping(dbapi_connection)
            except (jaydebeapi.DatabaseError, jpype.JException):
                return False

    jdbc_driver = 'com.alipay.oceanbase.jdbc.Driver'

    @property
    def jdbc_url(self):
        return 'jdbc:oceanbase://{NAME}'.format(**self.settings_dict)

    def init_connection_state(self):
        # TODO: custom OceanBase connection initialization
        pass
