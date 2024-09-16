import importlib

try:
    importlib.import_module("psycopg")

    from sqlalchemy.dialects.postgresql.psycopg import PGDialect_psycopg as PGDialect
except ModuleNotFoundError:
    from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2 as PGDialect

from dj_db_conn_pool.core.mixins import DatabasePoolWrapperMixin


class PGDatabaseWrapperMixin(DatabasePoolWrapperMixin):
    class SQLAlchemyDialect(PGDialect):
        pass

    def get_new_connection(self, conn_params):
        connection = super().get_new_connection(conn_params)

        connection.info = connection.driver_connection.info

        return connection
