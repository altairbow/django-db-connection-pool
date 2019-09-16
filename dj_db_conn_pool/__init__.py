__version__ = '1.0.2'
__author__ = 'Altair Bow'
__author_email__ = 'altair.bow@foxmail.com'
__description__ = 'Persistent database connection backends for Django'


def setup(pool_size=10, max_overflow=10):
    from dj_db_conn_pool.core import pool_container

    pool_container.pool_default_params.update(
        pool_size=pool_size,
        max_overflow=max_overflow
    )
