from django.core.exceptions import ImproperlyConfigured

from dj_db_conn_pool.backends.jdbc.mixins import JDBCDatabaseWrapperMixin
from dj_db_conn_pool.core.base import BaseDatabasePoolWrapper


class DatabaseWrapper(JDBCDatabaseWrapperMixin, BaseDatabasePoolWrapper):
    @property
    def jdbc_driver(self):
        try:
            return self.settings_dict['JDBC_DRIVER']
        except KeyError:
            raise ImproperlyConfigured('no JDBC_DRIVER provided')

    @property
    def jdbc_url(self):
        try:
            return self.settings_dict['JDBC_URL']
        except KeyError:
            raise ImproperlyConfigured('no JDBC_URL provided')
