from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2

from dj_db_conn_pool.core.mixins import PersistentDatabaseWrapperMixin


class PGDatabaseWrapperMixin(PersistentDatabaseWrapperMixin):
    class SQLAlchemyDialect(PGDialect_psycopg2):
        pass

    def get_new_connection(self, conn_params):
        connection = super().get_new_connection(conn_params)

        if not connection.info:
            connection.info = connection.connection.info

        return connection
