# -*- coding: utf-8 -*-

import jpype
import jaydebeapi
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.oracle import base
from sqlalchemy.dialects.mysql.base import MySQLDialect
from sqlalchemy.dialects.oracle.base import OracleDialect
from dj_db_conn_pool.backends.jdbc import JDBCDatabaseWrapperMixin


import logging
logger = logging.getLogger(__name__)


class DatabaseWrapper(JDBCDatabaseWrapperMixin, base.DatabaseWrapper):
    vendor = 'OceanBase'

    OceanBase_Mode_Oracle = 'Oracle'

    OceanBase_Mode_MySQL = 'MySQL'

    def _get_dialect(self, *args, **kwargs):
        ob_mode = self.settings_dict.get('OB_MODE', self.OceanBase_Mode_Oracle)

        if ob_mode == self.OceanBase_Mode_Oracle:
            dialect_class = OracleDialect
        elif ob_mode == self.OceanBase_Mode_MySQL:
            dialect_class = MySQLDialect
        else:
            raise ImproperlyConfigured(f'Not supported mode of OceanBase: {ob_mode}')

        class Dialect(dialect_class):
            def do_ping(self, dbapi_connection):
                try:
                    return super(dialect_class, self).do_ping(dbapi_connection)
                except (jaydebeapi.DatabaseError, jpype.JException):
                    return False

        return Dialect(dbapi=self.Database)

    jdbc_driver = 'com.alipay.oceanbase.jdbc.Driver'

    @property
    def jdbc_url(self):
        return 'jdbc:oceanbase://{NAME}'.format(**self.settings_dict)

    def init_connection_state(self):
        # TODO: custom OceanBase connection initialization
        pass
