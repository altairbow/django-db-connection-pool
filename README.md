# django-db-connection-pool

:star: If this project is helpful to you, please light up the star, Thank you:smile:

MySQL & Oracle & PostgreSQL & JDBC (Oracle, OceanBase) connection pool components for Django,
Be based on [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy).
Works fine in multiprocessing and multithreading django project.

* [中文版](README_CN.md)

## Quickstart

### Installation

Install with `pip` with all engines:

```bash
$ pip install django-db-connection-pool[all]
```

or select specific engines:

```bash
$ pip install django-db-connection-pool[mysql,oracle,postgresql,jdbc]
```

or one of mysql,oracle,postgresql,jdbc

```bash
$ pip install django-db-connection-pool[oracle]
```

### Update settings.DATABASES

#### MySQL

change `django.db.backends.mysql` to `dj_db_conn_pool.backends.mysql`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.mysql'
    }
}
```

#### Oracle

change `django.db.backends.oracle` to `dj_db_conn_pool.backends.oracle`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.oracle'
    }
}
```

#### PostgreSQL

change `django.db.backends.postgresql` to `dj_db_conn_pool.backends.postgresql`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.postgresql'
    }
}
```

#### Pool options(optional)

you can provide additional options to pass to SQLAlchemy's pool creation, key's name is `POOL_OPTIONS`:

```python
import logging

DATABASES = {
    'default': {
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': 10,
            'RECYCLE': 24 * 60 * 60,
            'LOG_LEVEL': logging.DEBUG
        }
    }
}

# or you can define logger under 'LOGGING' for dj_db_conn_pool settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'dj_db_conn_pool': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

```

`django-db-connection-pool` has more configuration options
here: [PoolContainer.pool_default_params](https://github.com/altairbow/django-db-connection-pool/blob/master/dj_db_conn_pool/core/__init__.py#L13-L20)

Here's the explanation of these options(from SQLAlchemy's Doc):

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

* **recycle**: If set to a value other than -1, number of seconds
  between connection recycling, which means upon checkout,
  if this timeout is surpassed the connection will be closed
  and replaced with a newly opened connection.
  Defaults to -1.

Or, you can use dj_db_conn_pool.setup to change default arguments(for each pool's creation), before using database pool:

```python
import dj_db_conn_pool

dj_db_conn_pool.setup(pool_size=100, max_overflow=50)
```

#### multiprocessing environment

In a multiprocessing environment, such as uWSGI, each process will have its own `dj_db_conn_pool.core:pool_container`
object,
It means that each process has an independent connection pool, for example:
The `POOL_OPTIONS` configuration of database `db1` is`{ 'POOL_SIZE': 10, 'MAX_OVERFLOW': 20 }`,
If uWSGI starts 8 worker processes, then the total connection pool size of `db1`  is `8 * 10`,
The maximum number of connections will not exceed `8 * 10 + 8 * 20`

## JDBC

Thanks to [JPype](https://github.com/jpype-project/jpype),
django-db-connection-pool can connect to database by jdbc

### Usage

#### Set Java runtime environment

```bash
export JAVA_HOME=$PATH_TO_JRE;
export CLASSPATH=$PATH_RO_JDBC_DRIVER_JAR
```

#### Update settings.DATABASES

##### Oracle

change `django.db.backends.oracle` to `dj_db_conn_pool.backends.jdbc.oracle`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.jdbc.oracle'
    }
}
```

##### OceanBase

use `dj_db_conn_pool.backends.jdbc.oceanbase`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.jdbc.oceanbase'
    }
}
```

### Performing raw SQL queries

Just like django's built-in backends, all JDBC backends support named parameters in raw SQL queries,
you can execute raw sql queries like this:

```python
from django.db import connections

with connections["default"].cursor() as cursor:
    cursor.execute('select name, phone from users where name = %(name)s', params={"name": "Altair"})
    result = cursor.fetchall()
```

### Acknowledgments
- Thanks to all friends who provided PR and suggestions !
- Thanks to [JetBrains](https://www.jetbrains.com/?from=django-db-connection-pool) for providing development tools for django-db-connection-pool !
