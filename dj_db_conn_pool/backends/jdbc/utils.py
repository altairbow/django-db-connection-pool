import logging
import sqlparams

logger = logging.getLogger(__name__)


class CursorWrapper:
    def __init__(self, cursor):
        self.cursor = cursor

        self._sql_params_converter = sqlparams.SQLParams('pyformat', 'qmark', True, True)

        self.statement = None

    def execute(self, query, parameters=None):
        if isinstance(parameters, dict):
            query, parameters = self._sql_params_converter.format(query, parameters)
        else:
            query = query.replace('%s', '?')

        self.statement = query

        return self.cursor.execute(query, parameters)

    def __getattr__(self, attr):
        return getattr(self.cursor, attr)

    def __iter__(self):
        return iter(self.cursor)
