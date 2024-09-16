import pyodbc
from django.conf import ImproperlyConfigured

from dj_db_conn_pool.core.mixins import DatabasePoolWrapperMixin


class ODBCDatabaseWrapperMixin(DatabasePoolWrapperMixin):
    Database = pyodbc

    def _get_new_connection(self, conn_params):
        try:
            driver = self.settings_dict['ODBC_OPTIONS']['DRIVER']
        except KeyError:
            raise ImproperlyConfigured('No odbc driver provided')

        conn_str_template = 'DRIVER={DRIVER};SERVER={HOST}:{PORT};DATABASE={NAME};UID={USER};PWD={PASSWORD}'

        connection_string = conn_str_template.format(DRIVER=driver, **self.settings_dict)

        return pyodbc.connect(connection_string)
