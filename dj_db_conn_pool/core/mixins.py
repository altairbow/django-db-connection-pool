# -*- coding: utf-8 -*-

from copy import deepcopy
from sqlalchemy import pool
from django.utils.translation import ugettext_lazy as _
from dj_db_conn_pool.core import pool_container


import logging
logger = logging.getLogger(__name__)


class PooledDatabaseWrapperMixin(object):
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
            # acquire the lock, check whether there exists the pool of this database
            if not pool_container.has(self.alias):
                # self.alias's pool doesn't exist, time to create it

                # make a copy of default parameters
                pool_params = deepcopy(pool_container.pool_default_params)

                # 开始解析、组装当前数据库的连接配置
                pool_setting = {
                    # 把 POOL_OPTIONS 内的参数名转换为小写
                    # 与 QueuePool 的参数对应
                    key.lower(): value
                    # 取每个 POOL_OPTIONS 内参数
                    for key, value in
                    # self.settings_dict 由 Django 提供，是 self.alias 的连接参数
                    self.settings_dict.get('POOL_OPTIONS', {}).items()
                    # 此处限制 POOL_OPTIONS 内的参数：
                    # POOL_OPTIONS 内的参数名必须是大写的
                    # 而且其小写形式必须在 pool_default_params 内
                    if key == key.upper() and key.lower() in pool_container.pool_default_params
                }

                # 现在 pool_setting 已经组装完成
                # 覆盖 pool_params 的参数（以输入用户的配置）
                pool_params.update(**pool_setting)

                # 现在参数已经具备
                # 创建 self.alias 的连接池实例
                alias_pool = pool.QueuePool(
                    # QueuePool 的 creator 参数
                    # 在获取一个新的数据库连接时，SQLAlchemy 会调用这个匿名函数
                    lambda: super(PooledDatabaseWrapperMixin, self).get_new_connection(conn_params),
                    # 数据库方言
                    # 用于 SQLAlchemy 维护该连接池
                    dialect=self.SQLAlchemyDialect(dbapi=self.Database),
                    # 自定义参数
                    **pool_params
                )

                logger.debug(_("%s's pool has been created, parameter: %s"), self.alias, pool_params)

                # 数据库连接池已创建
                # 放到 pool_container，以便重用
                pool_container.put(self.alias, alias_pool)

        # SQLAlchemy 连接池
        db_pool = pool_container.get(self.alias)
        # 从连接池取连接
        conn = db_pool.connect()
        logger.debug(_("got %s's connection from its pool"), self.alias)
        return conn

    def close(self, *args, **kwargs):
        logger.debug(_("release %s's connection to its pool"), self.alias)
        return super(PooledDatabaseWrapperMixin, self).close(*args, **kwargs)
