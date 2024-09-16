import getpass
import logging
import platform
import socket
from multiprocessing import current_process

from django.db.backends.oracle import base
from sqlalchemy.dialects.oracle.base import OracleDialect

from dj_db_conn_pool.backends.jdbc.mixins import JDBCDialectMixin, JDBCDatabaseWrapperMixin

logger = logging.getLogger(__name__)

oracle_session_info = {
    'v$session.process': str(current_process().pid),
    'v$session.osuser': getpass.getuser(),
    'v$session.machine': socket.gethostname(),
    'v$session.program': 'python.exe' if platform.system() == 'Windows' else 'python',
}


class DatabaseWrapper(JDBCDatabaseWrapperMixin, base.DatabaseWrapper):
    class SQLAlchemyDialect(JDBCDialectMixin, OracleDialect):
        pass

    jdbc_driver = 'oracle.jdbc.OracleDriver'

    jdbc_url_prefix = 'jdbc:oracle:thin:@'

    def get_connection_params(self):
        return {
            **oracle_session_info,
            **super().get_connection_params()
        }
