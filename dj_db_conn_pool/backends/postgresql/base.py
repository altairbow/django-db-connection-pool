# -*- coding: utf-8 -*-

from django.db.backends.postgresql import base
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin


class DatabaseWrapper(PooledDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(PGDialect_psycopg2):
        pass
