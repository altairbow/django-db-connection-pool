# -*- coding: utf-8 -*-

from django.db.backends.oracle import base
from sqlalchemy.dialects.oracle.base import OracleDialect
from dj_db_conn_pool.core.mixins import PersistentDatabaseWrapperMixin


class DatabaseWrapper(PersistentDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(OracleDialect):
        pass
