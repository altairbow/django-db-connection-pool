from django.db.backends.oracle import base
from dj_db_conn_pool.backends import BaseDatabaseWrapper


class DatabaseWrapper(BaseDatabaseWrapper, base.DatabaseWrapper):
    pass
