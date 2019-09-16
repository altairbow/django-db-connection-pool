# django-db-connection-pool

MySQL & Oracle connection pool backends of Django, Be based on SQLAlchemy.


#### Quickstart
1. Install with `pip`:
    ```bash
    $ pip install django-db-connection-pool
    ```

2. Configuration
    * ##### MySQL  
        change `django.db.backends.mysql` to `dj_db_conn_pool.backends.mysql`:
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
        change `django.db.backends.oracle` to `dj_db_conn_pool.backends.oracle`:
        ```
        DATABASES = {
            'default': {
                ...
                'ENGINE': 'dj_db_conn_pool.backends.oracle'
                ...
            }
        }
        ```
    * ##### pool options(optional)
        you can provide additional options to pass to SQLAlchemy's pool creation, key's name is `POOL_OPTIONS`:
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
        
        Here's explanation of these options(from SQLAlchemy's Doc):
        
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
                  
        or you can use dj_db_conn_pool.setup to change default arguments(for each pool's creation), before using database pool:
        ```python
        import dj_db_conn_pool
        dj_db_conn_pool.setup(pool_size=100, max_overflow=50)
        ```
