# -*- coding: utf-8 -*-

import types
import jaydebeapi
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin

import logging
logger = logging.getLogger(__name__)


class JDBCDatabaseWrapper(PooledDatabaseWrapperMixin):
    @property
    def jdbc_driver(self):
        raise NotImplementedError()

    @property
    def jdbc_url(self):
        raise NotImplementedError()

    @property
    def jdbc_options(self):
        return self.settings_dict.get('JDBC_OPTIONS', {})

    def _get_new_connection(self, conn_params):
        conn = jaydebeapi.connect(
            self.jdbc_driver,
            self.jdbc_url,
            {
                'user': self.settings_dict['USER'],
                'password': self.settings_dict['PASSWORD'],
                **self.jdbc_options
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
        return 'JDBC connection to {NAME}'.format(**self.settings_dict)

    __repr__ = __str__

    def _close(self):
        if self.connection is not None and self.connection.connection.jconn.getAutoCommit():
            # if jdbc connection's autoCommit is on
            # jaydebeapi will throw an exception after rollback called
            # we make a little dynamic patch here, make sure
            # SQLAlchemy will not do rollback before recycling connection
            self.connection._pool._reset_on_return = None

            logger.warning(
                "current JDBC connection(to %s)'s autoCommit is on, won't do rollback before returning",
                self.alias)
