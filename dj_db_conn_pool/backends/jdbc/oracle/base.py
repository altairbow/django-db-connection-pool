# -*- coding: utf-8 -*-

import getpass
import socket
from multiprocessing import current_process
import jpype
import jaydebeapi
from django.db.backends.oracle import base
from copy import deepcopy
from sqlalchemy.dialects.oracle.base import OracleDialect
from dj_db_conn_pool.backends.jdbc import JDBCDatabaseWrapper


import logging
logger = logging.getLogger(__name__)

oracle_session_info = {
    'v$session.process': str(current_process().pid),
    'v$session.osuser': getpass.getuser(),
    'v$session.machine': socket.gethostname(),
    'v$session.program': 'python',
}


class DatabaseWrapper(JDBCDatabaseWrapper, base.DatabaseWrapper):
    class SQLAlchemyDialect(OracleDialect):
        def do_ping(self, dbapi_connection):
            try:
                return super(OracleDialect, self).do_ping(dbapi_connection)
            except (jaydebeapi.DatabaseError, jpype.JException):
                return False

    jdbc_driver = 'oracle.jdbc.OracleDriver'

    @property
    def jdbc_url(self):
        return 'jdbc:oracle:thin:@//{NAME}'.format(**self.settings_dict)

    @property
    def jdbc_options(self):
        # make a copy of default option, avoid side effects
        jdbc_options = deepcopy(oracle_session_info)
        # get super's jdbc_options
        options = super(DatabaseWrapper, self).jdbc_options
        # override default options
        jdbc_options.update(**options)

        return jdbc_options
