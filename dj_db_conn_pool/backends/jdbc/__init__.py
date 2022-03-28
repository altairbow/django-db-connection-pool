# -*- coding: utf-8 -*-

import types
import jaydebeapi
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin

import logging
logger = logging.getLogger(__name__)


class JDBCDatabaseWrapper(PooledDatabaseWrapperMixin):
    JDBC_DRIVER = None

    def _get_jdbc_driver(self):
        if self.JDBC_DRIVER is None:
            raise NotImplementedError()

        return self.JDBC_DRIVER

    def _get_jdbc_url(self):
        raise NotImplementedError()

    def _get_jdbc_options(self):
        return self.settings_dict.get('JDBC_OPTIONS', {})

    def _get_new_connection(self, conn_params):
        conn = jaydebeapi.connect(
            self._get_jdbc_driver(),
            self._get_jdbc_url(),
            {
                'user': self.settings_dict['USER'],
                'password': self.settings_dict['PASSWORD'],
                **self._get_jdbc_options()
            }
        )

        return conn

    def create_cursor(self, name=None):
        """
        create a cursor
        just for compatibility
        :param name:
        :return:
        """
        # get cursor from django
        cursor = super().create_cursor(name)

        # just for compatibility
        cursor.setinputsizes = types.MethodType(lambda *_: None, cursor)

        def _execute(_self, query, *_args):
            # replace placeholder
            query = query.replace('%s', '?')

            # record last query
            cursor.statement = query

            # call jaydebeapi
            _self.cursor.execute(query, *_args)

        # just for compatibility
        cursor.execute = types.MethodType(_execute, cursor)

        return cursor

    def __str__(self):
        return 'JDBC Connection to {NAME}'.format(**self.settings_dict)

    __repr__ = __str__
