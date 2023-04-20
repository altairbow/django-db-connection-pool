# django-db-connection-pool

*:star: 如果这个库能对你有所帮助，不妨点个star，谢谢:smile:*

驱动 Django 访问 MySQL、Oracle、PostgreSQL、JDBC (Oracle, OceanBase) 连接池的轮子, 
基于 [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) 队列池。
在多进程、多线程 django 项目中，运行良好。

* [English version](README.md)

## 快速开始
### 安装
+ 使用 `pip` 安装所有所支持的数据库组件:
```bash
$ pip install django-db-connection-pool[all]
```
+ 或者是选择性安装数据库组件:
```bash
$ pip install django-db-connection-pool[mysql,oracle,postgresql,jdbc]
```
+ 或只选择部分组件，比如 Oracle
```bash
$ pip install django-db-connection-pool[oracle]
```

### 更新 settings.DATABASES 配置

#### MySQL  
将 ENGINE `django.db.backends.mysql` 更改为 `dj_db_conn_pool.backends.mysql`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.mysql',
        "NAME": "db1",
        "USER": "user",
        "PASSWORD": "password",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "POOL_OPTIONS": {
          "POOL_SIZE": 10,
          "MAX_OVERFLOW": 10
        }
    }
}
```

#### Oracle
将 ENGINE `django.db.backends.oracle` 更改为 `dj_db_conn_pool.backends.oracle`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.oracle',
        "NAME": "db1",
        "USER": "user",
        "PASSWORD": "password",
        "HOST": "127.0.0.1",
        "PORT": "1521",
        "POOL_OPTIONS": {
          "POOL_SIZE": 10,
          "MAX_OVERFLOW": 10
        }
    }
}
```

#### PostgreSQL  
将 ENGINE `django.db.backends.postgresql` 更改为 `dj_db_conn_pool.backends.postgresql`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.postgresql',
        "NAME": "db1",
        "USER": "user",
        "PASSWORD": "password",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "POOL_OPTIONS": {
          "POOL_SIZE": 10,
          "MAX_OVERFLOW": 10
        }
    }
}
```

#### 连接池配置（可选）
目前连接池限制用户传入的连接池配置为：POOL_SIZE（连接池容量）、MAX_OVERFLOW（连接池容量向上浮动最大值）
这两个参数包含在 `POOL_OPTIONS` 内，例如下面的配置，default 的连接池常规容量为10个连接，最大浮动10个，
即为：在 default 连接池创建后，随着程序对连接池的请求，连接池内连接将逐步增加到10个，如果在连接池内连接
全部用光后，程序又请求了第11个连接，此时的连接池容量将短暂超过 POOL_SIZE，但最大不超过 POOL_SIZE + MAX_OVERFLOW，
如果程序请求 default 数据库的连接数量超过 POOL_SIZE + MAX_OVERFLOW，那么连接池将一直等待直到程序释放连接，
请注意线程池对数据库连接池的使用，如果线程池大于连接池，且线程无主动释放连接的动作，可能会造成其他线程一直阻塞。

```python
DATABASES = {
    'default': {
        'POOL_OPTIONS' : {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': 10,
            'RECYCLE': 24 * 60 * 60,
            'PRE_PING': True,
            'ECHO': False,
            'TIMEOUT': 30,
        }
     }
 }
```

附这些参数的解释：(摘录于 SQLAlchemy 的文档):

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

或者调用 `dj_db_conn_pool.setup` 覆盖默认参数

```python
import dj_db_conn_pool
dj_db_conn_pool.setup(pool_size=10, max_overflow=20)
```

#### 多进程环境
在多进程环境内，每个进程都会拥有一个`dj_db_conn_pool.core:pool_container`对象， 意味着每个进程都拥有一个独立的连接池，举例说明：  
数据库`db1`的`POOL_OPTIONS`的配置是
`{ 'POOL_SIZE': 10, 'MAX_OVERFLOW': 20 }`，项目启动了8个进程，则该项目的`db1`连接池总大小是`8 * 10`，最大连接数是`8 * 10 + 8 * 20`

## JDBC（仍在完善中，不建议用于生产）
基于 [JPype](https://github.com/jpype-project/jpype)，django-db-connection-pool 现在可以通过 jdbc 连接到数据库并保持连接

### 使用方法
#### 设置环境变量
```bash
export JAVA_HOME=$PATH_TO_JRE;
export CLASSPATH=$PATH_RO_JDBC_DRIVER_JAR
```

#### 更新 settings.DATABASES 配置
##### Oracle

将 ENGINE `django.db.backends.oracle` 更改为 `dj_db_conn_pool.backends.jdbc.oracle`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.jdbc.oracle',
        "NAME": "db1",
        "USER": "user",
        "PASSWORD": "password",
        "HOST": "127.0.0.1",
        "PORT": "1521",
        "POOL_OPTIONS": {
          "POOL_SIZE": 10,
          "MAX_OVERFLOW": 10
        }
    }
}
```

##### OceanBase
使用 `dj_db_conn_pool.backends.jdbc.oceanbase` 作为 Django 数据库后端:
```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.jdbc.oceanbase',
        "NAME": "db1",
        "USER": "user",
        "PASSWORD": "password",
        "HOST": "127.0.0.1",
        "PORT": "2881",
        "POOL_OPTIONS": {
          "POOL_SIZE": 10,
          "MAX_OVERFLOW": 10
        }
    }
}
```
