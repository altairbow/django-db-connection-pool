import threading
from copy import deepcopy
from sqlalchemy import pool

import logging
logger = logging.getLogger(__name__)

# map for holding database QueuePool of current/every process
# looks like {'db.user': QueuePool(**kwargs), ...}
database_pool_dict = {}

# Lock for modifying connection pools
# when we modifying database_pool_dict
# we will require pool_modify_mutex
pool_modify_mutex = threading.Lock()

# default parameters for QueuePool
pool_default_params = {
    'pool_size': 10,
    'max_overflow': 10,
    'pre_ping': True
}


class BaseDatabaseWrapper:
    def get_new_connection(self, conn_params):
        """
        django use this method for get database connection,
        django open a database connection for a session and won't reuse it
        we override this method, replace django's default action,
        when django want to get a database connection, we get one from the pool
        and return to django, after django finish one request/response, django
        will call .close(), then we can reuse every database connection
        :param conn_params: database connection parameters
        :return:
        """
        with pool_modify_mutex:
            # self.alias is database's alias
            # like: {'default': {}}, self.alias is 'default'
            if self.alias not in database_pool_dict:
                # alias's pool is not initialized
                # we will parse it's parameters
                # and initialize it

                # copy default parameters
                pool_params = deepcopy(pool_default_params)

                # parse alias's setting
                pool_setting = {
                    # get key's lower
                    key.lower(): value
                    # get key & value
                    for key, value in
                    self.settings_dict.get('POOL', {}).items()
                    # we check key whether key eq it's upper
                    # means key must be CAPITALIZED
                    # and key.upper() must in pool_params
                    if key == key.upper() and key.lower() in pool_params
                }

                # merge default and setting
                pool_params.update(**pool_setting)

                # create a QueuePool instance
                # and
                alias_pool = pool.QueuePool(
                    # django provides super().get_new_connection method
                    # accept 'conn_params', and return a db-api Connection
                    # we pass a lambda to QueuePool
                    lambda: super(BaseDatabaseWrapper, self).get_new_connection(conn_params),
                    # dbapi dialect
                    dialect=self.SQLAlchemyDialect(dbapi=self.Database),
                    # QueuePool pool_params
                    echo=True, timeout=None, **pool_params
                )

                logger.debug('%s database pool initialized, parameters: %s',
                             self.alias, pool_params)

                # database pool initialized
                # put into map
                database_pool_dict[self.alias] = alias_pool

        conn = database_pool_dict[self.alias].connect()
        logger.debug('got %s database connection', self.alias)
        return conn

    def close(self, *args, **kwargs):
        logger.debug('release %s database connection to pool', self.alias)
        return super(BaseDatabaseWrapper, self).close(*args, **kwargs)
