__version__ = '1.1.0'
__author__ = 'Altair Bow'
__author_email__ = 'altair.bow@foxmail.com'
__description__ = 'Persistent database connection backends for Django'


def setup(**kwargs):
    from dj_db_conn_pool.core import pool_container

    for key, value in kwargs.items():
        if key in pool_container.pool_default_params:
            pool_container.pool_default_params[key] = value
