# -*- coding: utf-8 -*-

from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2
from dj_db_conn_pool.core.mixins import PersistentDatabaseWrapperMixin


class PGDatabaseWrapperMixin(PersistentDatabaseWrapperMixin):
    class SQLAlchemyDialect(PGDialect_psycopg2):
        pass
