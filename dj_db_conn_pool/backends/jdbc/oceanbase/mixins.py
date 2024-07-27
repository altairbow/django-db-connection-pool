from dj_db_conn_pool.backends.jdbc import JDBCDatabaseWrapperMixin


class JDBCOceanBaseDatabaseWrapperMixin(JDBCDatabaseWrapperMixin):
    vendor = 'OceanBase'

    jdbc_driver = 'com.oceanbase.jdbc.driver'

    jdbc_url_prefix = 'jdbc:oceanbase:'
