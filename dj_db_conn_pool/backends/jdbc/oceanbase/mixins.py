# -*- coding: utf-8 -*-

from dj_db_conn_pool.backends.jdbc import JDBCDatabaseWrapperMixin


class JDBCOceanBaseDatabaseWrapperMixin(JDBCDatabaseWrapperMixin):
    vendor = 'OceanBase'

    jdbc_driver = 'com.alipay.oceanbase.jdbc.Driver'

    jdbc_url_prefix = 'jdbc:oceanbase:'
