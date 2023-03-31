# -*- coding: utf-8 -*-

from django.contrib.gis.db.backends.postgis import base
from sqlalchemy.dialects.postgresql.base import PGDialect
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin


class DatabaseWrapper(PooledDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(PGDialect):
        pass
