import threading
from copy import deepcopy
from sqlalchemy import pool

import logging
logger = logging.getLogger(__name__)

# 保存各个数据库的池（QueuePool）实例
database_pool_dict = {}

# 修改 database_pool_dict 时需要请求的锁
pool_modify_mutex = threading.Lock()

# 池的默认参数
pool_default_params = {
    'pool_size': 10,
    'max_overflow': 10
}


class BaseDatabaseWrapper:
    def get_new_connection(self, conn_params):
        """
        覆盖 Django 的 get_new_connection 方法
        在 Django 调用 此方法时，检查 database_pool_dict 中是否有 self.alias 的连接池
        如果没有，则初始化 self.alias 的连接池，然后从池中取出一个连接
        如果有，则直接从池中取出一个连接返回
        :return:
        """
        with pool_modify_mutex:
            # 获取锁后，判断当前数据库（self.alias）的池是否存在
            # 不存在，开始初始化
            if self.alias not in database_pool_dict:
                # 复制一份默认参数给当前数据库
                pool_params = deepcopy(pool_default_params)
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
                    if key == key.upper() and key.lower() in pool_default_params
                }

                # 现在 pool_setting 已经组装完成
                # 覆盖 pool_params 的参数（以输入用户的配置）
                pool_params.update(**pool_setting)

                # 现在参数已经具备
                # 创建 self.alias 的连接池实例
                alias_pool = pool.QueuePool(
                    # QueuePool 的 creator 参数
                    # 我们利用 django 的 get_new_connection 方法
                    # “告诉” QueuePool 怎么去创建一个新的数据库连接
                    # 在获取一个新的数据库连接时，SQLAlchemy 会调用这个 lambda
                    lambda: super(BaseDatabaseWrapper, self).get_new_connection(conn_params),
                    # 数据库“方言”
                    # 在这里的作用主要作用是给 SQLAlchemy 利用
                    # 判断数据库连接的状态，以便 SQLAlchemy 维护该连接池
                    dialect=self.SQLAlchemyDialect(dbapi=self.Database),
                    # 一些固定的参数
                    pre_ping=True, echo=True, timeout=None, **pool_params
                )

                logger.debug('%s 数据库连接池已创建, 参数: %s',
                             self.alias, pool_params)

                # 数据库连接池已创建
                # 放到 database_pool_dict，以便重用
                database_pool_dict[self.alias] = alias_pool

        # 调用 SQLAlchemy 从连接池内取一个连接
        conn = database_pool_dict[self.alias].connect()
        logger.debug('从池中获取到 %s 数据库的连接', self.alias)
        return conn

    def close(self, *args, **kwargs):
        logger.debug('释放 %s 数据库连接到池中', self.alias)
        return super(BaseDatabaseWrapper, self).close(*args, **kwargs)
