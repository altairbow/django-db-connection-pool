from django.db.backends.postgresql import base

from dj_db_conn_pool.backends.postgresql.mixins import PGDatabaseWrapperMixin


class DatabaseWrapper(PGDatabaseWrapperMixin, base.DatabaseWrapper):
    pass
