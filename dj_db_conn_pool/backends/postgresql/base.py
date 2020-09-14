# -*- coding: utf-8 -*-

from django.db.backends.postgresql_psycopg2 import base
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin


class DatabaseWrapper(PooledDatabaseWrapperMixin, base.DatabaseWrapper):
    class PostgreSQLDialect(PGDialect):
        pass