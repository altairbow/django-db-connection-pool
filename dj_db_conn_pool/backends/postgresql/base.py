# -*- coding: utf-8 -*-

from django.db.backends.postgresql import base
from dj_db_conn_pool.backends.postgresql.mixins import PGDatabaseWrapperMixin


class DatabaseWrapper(PGDatabaseWrapperMixin, base.DatabaseWrapper):
    def get_new_connection(self, conn_params):
        connection = super().get_new_connection(conn_params)

        if not connection.info:
            connection.info = connection.connection.info

        return connection
