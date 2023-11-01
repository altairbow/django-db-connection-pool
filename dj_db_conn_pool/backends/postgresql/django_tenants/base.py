from django_tenants.postgresql_backend import base

from dj_db_conn_pool.backends.postgresql.mixins import PGDatabaseWrapperMixin


class DatabaseWrapper(PGDatabaseWrapperMixin, base.DatabaseWrapper):
    """
    Notice: this backend is only available for django_tenants
    """
    pass
