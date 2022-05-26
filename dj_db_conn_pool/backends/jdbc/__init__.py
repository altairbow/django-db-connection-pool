# -*- coding: utf-8 -*-

import types
import sqlparams
import jaydebeapi
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin

import logging
logger = logging.getLogger(__name__)

sql_params = sqlparams.SQLParams('named', 'qmark')


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
        do some tricks here
        :param name:
        :return:
        """
        # get cursor from django
        cursor = super().create_cursor(name)

        def _execute(_self, query, parameters=None):
            """
            :param _self: django's cursor
            :param query: SQL
            :param parameters: SQL parameters
            :return:
            """
            if isinstance(parameters, dict):
                # convert sql and parameters
                _query, _parameters = sql_params.format(query, parameters)

                logger.debug(
                    'SQL (%s), parameters(%s) has been converted to SQL(%s), parameters(%s)',
                    query, parameters, _query, _parameters)

                query, parameters = (_query, _parameters)
            else:
                # change paramstyle 'format' to 'qmark'
                query = query.replace('%s', '?')

            # record last query
            cursor.statement = query

            # call jaydebeapi
            _self.cursor.execute(query, parameters)

        # replace django cursor's execute method
        cursor.execute = types.MethodType(_execute, cursor)

        return cursor

    def _close(self):
        if self.connection is not None and self.connection.connection.jconn.getAutoCommit():
            # if jdbc connection's autoCommit is on
            # jaydebeapi will throw an exception after rollback called
            # we make a little dynamic patch here, make sure
            # SQLAlchemy will not do rollback before recycling connection
            self.connection._pool._reset_on_return = None

            logger.debug(
                "autoCommit of current JDBC connection to %s %s is on, won't do rollback before returning",
                self.alias, self.connection.connection)

        return super(JDBCDatabaseWrapper, self)._close()
