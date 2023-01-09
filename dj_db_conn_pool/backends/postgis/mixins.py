# -*- coding: utf-8 -*-

from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin


class PGDatabaseWrapperMixin(PooledDatabaseWrapperMixin):
    class SQLAlchemyDialect(PGDialect_psycopg2):
        pass
