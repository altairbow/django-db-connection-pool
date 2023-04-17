# -*- coding: utf-8 -*-

from django.db.backends.oracle import base
from sqlalchemy.dialects.oracle.base import OracleDialect
from dj_db_conn_pool.core.mixins import PersistentDatabaseWrapperMixin


class DatabaseWrapper(PersistentDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(OracleDialect):
        pass

    def _set_dbapi_autocommit(self, autocommit):
        self.connection.driver_connection.autocommit = int(autocommit)
