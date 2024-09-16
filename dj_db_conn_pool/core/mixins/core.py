import logging

from sqlalchemy import pool

from dj_db_conn_pool.compat import gettext_lazy as _
from dj_db_conn_pool.core import pool_container
from dj_db_conn_pool.core.mixins.creation import DatabaseCreationMixin

logger = logging.getLogger(__name__)


class DatabasePoolWrapperMixin:
    def __init__(self, *args, **kwargs):
        # override creation_class
        self.creation_class = type('DatabaseCreationWrapper', (DatabaseCreationMixin, self.creation_class), {})

        super().__init__(*args, **kwargs)

    def __str__(self):
        try:
            conn = repr(self.connection.driver_connection)
        except AttributeError:
            conn = '<Not connected>'

        return f'{self.vendor} connection to {self.alias}: {conn}'

    __repr__ = __str__

    def _set_dbapi_autocommit(self, autocommit):
        self.connection.driver_connection.autocommit = autocommit

    def _set_autocommit(self, autocommit):
        with self.wrap_database_errors:
            try:
                self._set_dbapi_autocommit(autocommit)
            except (Exception,) as exc:
                logger.exception('unable to set autocommit mode of %s(%s) to %s, caused by: %s',
                                 self.vendor, self.alias, autocommit, exc)
                raise exc from None

    def _get_dialect(self):
        return self.SQLAlchemyDialect(dbapi=self.Database)

    def _get_new_connection(self, conn_params):
        return super().get_new_connection(conn_params)

    def get_new_connection(self, conn_params):
        """
        override django.db.backends.<database>.base.DatabaseWrapper.get_new_connection to
        change the default behavior of getting new connection to database, we maintain
        pool_container who contains the connection pool of each database here
        when django call this method to get new connection, we check whether there exists
        the pool of this database(self.alias)
        if the target pool doesn't exist, we will create one
        then grab one connection from the pool and return it to django
        :return:
        """
        with pool_container.lock:
            # acquire the lock, check whether there exists the pool of current database
            # note: the value of self.alias is the name of current database, one of setting.DATABASES
            if not pool_container.has(self.alias):
                # self.alias's pool doesn't exist, time to create it

                # parse parameters of current database from self.settings_dict
                pool_setting = {
                    # transform the keys in POOL_OPTIONS to lower case
                    # to fit sqlalchemy.pool.QueuePool's arguments requirement
                    key.lower(): value
                    # traverse POOL_OPTIONS to get arguments
                    for key, value in
                    # self.settings_dict was created by Django
                    # is the connection parameters of self.alias
                    self.settings_dict.get('POOL_OPTIONS', {}).items()
                    # There are some limits of self.alias's pool's option(POOL_OPTIONS):
                    # the keys in POOL_OPTIONS must be capitalised
                    # and the key's lowercase must be in pool_container.pool_default_params
                    if key == key.upper() and key.lower() in pool_container.pool_default_params
                }

                # replace pool_params's items with pool_setting's items
                # to import custom settings
                pool_params = {
                    **pool_container.pool_default_params,
                    **pool_setting
                }

                # now we have all parameters of self.alias
                # create self.alias's pool
                alias_pool = pool.QueuePool(
                    lambda: self._get_new_connection(conn_params),
                    # SQLAlchemy use the dialect to maintain the pool
                    dialect=self._get_dialect(),
                    # parameters of self.alias
                    **pool_params
                )

                logger.debug(_("%s's pool has been created, parameter: %s"), self.alias, pool_params)

                # pool has been created
                # put into pool_container for reusing
                pool_container.put(self.alias, alias_pool)

        # get self.alias's pool from pool_container
        db_pool = pool_container.get(self.alias)
        # get one connection from the pool
        conn = db_pool.connect()

        logger.debug(
            _("got %s's connection %s from its pool"),
            self.alias, conn.driver_connection)

        return conn

    def close(self, *args, **kwargs):
        logger.debug(
            _("release %s's connection %s to its pool"),
            self.alias, getattr(self.connection, 'driver_connection', None))

        return super().close(*args, **kwargs)
