from dj_db_conn_pool.backends.jdbc.oceanbase.mixins import JDBCOceanBaseDatabaseWrapperMixin
from dj_db_conn_pool.core.base import BaseDatabasePoolWrapper


class DatabaseWrapper(JDBCOceanBaseDatabaseWrapperMixin, BaseDatabasePoolWrapper):
    pass
