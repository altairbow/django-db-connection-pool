# -*- coding: utf-8 -*-

# from django.db.backends.postgresql import base
from django.contrib.gis.db.backends.postgis import base as gis_base
from dj_db_conn_pool.backends.postgresql.mixins import PGDatabaseWrapperMixin


class DatabaseWrapper(PGDatabaseWrapperMixin, gis_base.DatabaseWrapper):
    pass
