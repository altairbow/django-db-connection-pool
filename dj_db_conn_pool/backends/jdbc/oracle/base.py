import getpass
import logging
import platform
import socket
from multiprocessing import current_process

import jpype.dbapi2
from django.db.backends.oracle import base
from sqlalchemy.dialects.oracle.base import OracleDialect

from dj_db_conn_pool.backends.jdbc import JDBCDatabaseWrapperMixin

logger = logging.getLogger(__name__)

oracle_session_info = {
    'v$session.process': str(current_process().pid),
    'v$session.osuser': getpass.getuser(),
    'v$session.machine': socket.gethostname(),
    'v$session.program': 'python.exe' if platform.system() == 'Windows' else 'python',
}


class DatabaseWrapper(JDBCDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(OracleDialect):
        def do_ping(self, dbapi_connection):
            try:
                return super().do_ping(dbapi_connection)
            except jpype.dbapi2.DatabaseError:
                return False

    jdbc_driver = 'oracle.jdbc.OracleDriver'

    jdbc_url_prefix = 'jdbc:oracle:thin:@'

    def get_connection_params(self):
        return {
            **oracle_session_info,
            **super().get_connection_params()
        }
