from django.contrib.gis.db.backends.postgis import base
from sqlalchemy.dialects.postgresql.base import PGDialect

from dj_db_conn_pool.backends.postgresql.mixins import PGDatabaseWrapperMixin


class DatabaseWrapper(PGDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(PGDialect):
        pass
