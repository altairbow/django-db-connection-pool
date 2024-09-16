from dj_db_conn_pool.backends.jdbc.mixins import JDBCDatabaseWrapperMixin


class JDBCOceanBaseDatabaseWrapperMixin(JDBCDatabaseWrapperMixin):
    vendor = 'OceanBase'

    jdbc_driver = 'com.oceanbase.jdbc.Driver'

    jdbc_url_prefix = 'jdbc:oceanbase:'
