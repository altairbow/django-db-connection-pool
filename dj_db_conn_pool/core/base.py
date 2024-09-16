import logging

from django.db.backends.base import base
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.backends.base.introspection import BaseDatabaseIntrospection
from django.db.backends.base.operations import BaseDatabaseOperations
from sqlalchemy.engine.default import DefaultDialect

from dj_db_conn_pool.core.mixins.core import DatabasePoolWrapperMixin

logger = logging.getLogger(__name__)


class BaseDatabasePoolWrapper(DatabasePoolWrapperMixin, base.BaseDatabaseWrapper):
    client_class = BaseDatabaseClient

    creation_class = BaseDatabaseCreation

    features_class = BaseDatabaseFeatures

    introspection_class = BaseDatabaseIntrospection

    ops_class = BaseDatabaseOperations

    class SQLAlchemyDialect(DefaultDialect):
        def do_ping(self, dbapi_connection):
            try:
                return super().do_ping(dbapi_connection)
            except self.Database.DatabaseError:
                return False

    def init_connection_state(self):
        pass
