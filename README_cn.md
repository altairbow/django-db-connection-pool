# django-db-connection-pool

驱动 Django MySQL、Oracle 连接池的轮子, 基于 SQLAlchemy 队列池

#### 快速开始
1. 使用 `pip` 进行:
    ```bash
    $ pip install django-db-connection-pool
    ```

2. 更新 DATABASES 的 配置
    * ##### MySQL  
        将 ENGINE `django.db.backends.mysql` 更改为 `dj_db_conn_pool.backends.mysql`:
        ```
        DATABASES = {
            'default': {
                ...
                'ENGINE': 'dj_db_conn_pool.backends.mysql'
                ...
            }
        }
        ```
    
    * ##### Oracle  
        将 ENGINE `django.db.backends.oracle` 更改为 `dj_db_conn_pool.backends.oracle`:
        ```
        DATABASES = {
            'default': {
                ...
                'ENGINE': 'dj_db_conn_pool.backends.oracle'
                ...
            }
        }
        ```
    * ##### 连接池配置（可选）
        目前连接池限制用户传入的连接池配置为：POOL_SIZE（连接池容量）、MAX_OVERFLOW（连接池容量上下浮动最大值）
        这两个参数包含在 `POOL_OPTIONS` 内，例如下面的配置，default 的连接池常规容量为10个连接，最大浮动10个，
        即为：在 default 连接池创建后，随着程序对连接池的请求，连接池内连接将逐步增加到10个，如果在连接池内连接
        全部用光后，程序又请求了第11个连接，此时的连接池容量将短暂超过 POOL_SIZE，但最大不超过 POOL_SIZE + MAX_OVERFLOW，
        如果程序请求 default 数据库的连接数量超过 POOL_SIZE + MAX_OVERFLOW，那连接池将一直等待直到程序释放连接。
        ```
        DATABASES = {
            'default': {
                ...
                'POOL_OPTIONS' : {
                    'POOL_SIZE': 10,
                    'MAX_OVERFLOW': 10
                }
                ...
             }
         }
        ```
        
        附这两个参数的解释：(摘录于 SQLAlchemy 的文档):
        
        * **pool_size**: The size of the pool to be maintained,
                  defaults to 5. This is the largest number of connections that
                  will be kept persistently in the pool. Note that the pool
                  begins with no connections; once this number of connections
                  is requested, that number of connections will remain.
                  `pool_size` can be set to 0 to indicate no size limit; to
                  disable pooling, use a :class:`~sqlalchemy.pool.NullPool`
                  instead.
        
        * **max_overflow**: The maximum overflow size of the
                  pool. When the number of checked-out connections reaches the
                  size set in pool_size, additional connections will be
                  returned up to this limit. When those additional connections
                  are returned to the pool, they are disconnected and
                  discarded. It follows then that the total number of
                  simultaneous connections the pool will allow is pool_size +
                  `max_overflow`, and the total number of "sleeping"
                  connections the pool will allow is pool_size. `max_overflow`
                  can be set to -1 to indicate no overflow limit; no limit
                  will be placed on the total number of concurrent
                  connections. Defaults to 10.
