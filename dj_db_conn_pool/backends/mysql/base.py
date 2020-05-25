# -*- coding: utf-8 -*-

from django.db.backends.mysql import base
from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql
from dj_db_conn_pool.core.mixins import PooledDatabaseWrapperMixin


class DatabaseWrapper(PooledDatabaseWrapperMixin, base.DatabaseWrapper):
    SQLAlchemyDialect = MySQLDialect_pymysql
