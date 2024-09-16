import logging
import threading

import jpype
import jpype.dbapi2

from dj_db_conn_pool.backends.jdbc.utils import CursorWrapper
from dj_db_conn_pool.core.mixins import DatabasePoolWrapperMixin

logger = logging.getLogger(__name__)

jdbc_type_converters = {}

lock_check_jvm_status = threading.Lock()


class JDBCDialectMixin:
    def do_ping(self, dbapi_connection):
        try:
            return super().do_ping(dbapi_connection)
        except jpype.dbapi2.DatabaseError:
            return False


class JDBCDatabaseWrapperMixin(DatabasePoolWrapperMixin):
    Database = jpype.dbapi2

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

    def create_cursor(self, name=None):
        cursor = self.connection.cursor()

        return CursorWrapper(cursor)

    def get_connection_params(self):
        return self.settings_dict.get('OPTIONS', {})

    def _get_new_connection(self, conn_params):
        with lock_check_jvm_status:
            if not jpype.isJVMStarted():
                jpype.startJVM(ignoreUnrecognized=True)

        conn = jpype.dbapi2.connect(
            self.jdbc_url,
            driver=self.jdbc_driver,
            driver_args=dict(
                user=self.settings_dict['USER'],
                password=self.settings_dict['PASSWORD'],
                **conn_params
            ),
            converters=jdbc_type_converters,
        )

        return conn

    def _close(self):
        if self.connection is not None and self.connection.driver_connection.autocommit:
            # if jdbc connection's autoCommit is on
            # jpype will throw NotSupportedError after rollback called
            # we make a little dynamic patch here, make sure
            # SQLAlchemy will not do rollback before recycling connection
            self.connection._pool._reset_on_return = None

            logger.debug(
                "autoCommit of current JDBC connection to %s %s is on, won't do rollback before returning",
                self.alias, self.connection.driver_connection)

        return super()._close()
