# -*- coding: utf-8 -*-

import jaydebeapi
from dj_db_conn_pool.core.mixins import PersistentDatabaseWrapperMixin
from dj_db_conn_pool.backends.jdbc.utils import CursorWrapper

import logging
logger = logging.getLogger(__name__)


class JDBCDatabaseWrapperMixin(PersistentDatabaseWrapperMixin):
    def _set_dbapi_autocommit(self, autocommit):
        self.connection.driver_connection.jconn.setAutoCommit(autocommit)

    @property
    def jdbc_driver(self):
        raise NotImplementedError()

    @property
    def jdbc_url_prefix(self):
        raise NotImplementedError()

    @property
    def jdbc_url(self):
        return '{prefix}//{HOST}:{PORT}/{NAME}'.format(
            prefix=self.jdbc_url_prefix,
            **self.settings_dict
        )

    def get_connection_params(self):
        return self.settings_dict.get('OPTIONS', {})

    def _get_new_connection(self, conn_params):
        conn = jaydebeapi.connect(
            self.jdbc_driver,
            self.jdbc_url,
            {
                'user': self.settings_dict['USER'],
                'password': self.settings_dict['PASSWORD'],
                **conn_params
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

        return CursorWrapper(cursor)

    def _close(self):
        if self.connection is not None and self.connection.driver_connection.jconn.getAutoCommit():
            # if jdbc connection's autoCommit is on
            # jaydebeapi will throw an exception after rollback called
            # we make a little dynamic patch here, make sure
            # SQLAlchemy will not do rollback before recycling connection
            self.connection._pool._reset_on_return = None

            logger.debug(
                "autoCommit of current JDBC connection to %s %s is on, won't do rollback before returning",
                self.alias, self.connection.driver_connection)

        return super(JDBCDatabaseWrapperMixin, self)._close()
