# -*- coding: utf-8 -*-

import threading
from dj_db_conn_pool.compat import gettext_lazy as _
from dj_db_conn_pool.core.exceptions import PoolDoesNotExist


class PoolContainer(dict):
    # acquire this lock before modify pool_container
    lock = threading.Lock()

    # the default parameters of pool
    pool_default_params = {
        'pre_ping': True,
        'echo': False,
        'timeout': 30,
        'recycle': 60 * 15,
        'pool_size': 10,
        'max_overflow': 10,
    }

    def has(self, pool_name):
        return pool_name in self

    def put(self, pool_name, pool):
        self[pool_name] = pool

    def get(self, pool_name):
        try:
            return self[pool_name]
        except KeyError:
            raise PoolDoesNotExist(_('No such pool: {pool_name}').format(pool_name=pool_name))


# the pool's container, for maintaining the pools
# every process has it's own pool container
pool_container = PoolContainer()
