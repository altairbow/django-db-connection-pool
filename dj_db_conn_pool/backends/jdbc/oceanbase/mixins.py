# -*- coding: utf-8 -*-

from django.db.backends.oracle import base
from dj_db_conn_pool.backends.jdbc import JDBCDatabaseWrapperMixin


class JDBCOceanBaseDatabaseWrapperMixin(JDBCDatabaseWrapperMixin, base.DatabaseWrapper):
    vendor = 'OceanBase'

    jdbc_driver = 'com.alipay.oceanbase.jdbc.Driver'

    @property
    def jdbc_url(self):
        return 'jdbc:oceanbase://{NAME}'.format(**self.settings_dict)
