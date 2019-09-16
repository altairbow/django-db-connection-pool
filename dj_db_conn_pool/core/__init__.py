# -*- coding: utf-8 -*-

import threading
from django.utils.translation import ugettext_lazy as _
from dj_db_conn_pool.core.exceptions import PoolDoesNotExist


class PoolContainer(dict):
    # 修改池容器时需要请求的锁
    lock = threading.Lock()

    # 单个数据库连接池的默认参数
    pool_default_params = {
        'pool_size': 10,
        'max_overflow': 10
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


# 池容器，保存各个数据库的池（QueuePool）实例
pool_container = PoolContainer()
