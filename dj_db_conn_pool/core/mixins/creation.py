# -*- coding: utf-8 -*-

from dj_db_conn_pool.core import pool_container


class DatabaseCreationMixin(object):
    def _destroy_test_db(self, test_database_name, verbosity):
        # dispose all pools before destroying testdb
        pool_container.dispose()

        # destroy testdb
        return super(DatabaseCreationMixin, self)._destroy_test_db(test_database_name, verbosity)
