# -*- coding: utf-8 -*-

import pyodbc
from dj_db_conn_pool.core.mixins import PersistentDatabaseWrapperMixin


class ODBCWrapperMixin(PersistentDatabaseWrapperMixin):
    def _get_new_connection(self, conn_params):
        conn = pyodbc.connect(
            '', **self.settings_dict
        )

        return conn
