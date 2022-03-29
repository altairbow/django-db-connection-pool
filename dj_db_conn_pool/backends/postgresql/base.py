# -*- coding: utf-8 -*-

from django.db.backends.postgresql import base
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin


class DatabaseWrapper(PooledDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(PGDialect_psycopg2):
        pass

    def _set_autocommit(self, autocommit):
        with self.wrap_database_errors:
            self.connection.dbapi_connection.autocommit = autocommit

    def __str__(self):
        return 'PostgreSQL connection to {NAME}'.format(**self.settings_dict)

    __repr__ = __str__
