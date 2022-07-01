import sqlparams

import logging
logger = logging.getLogger(__name__)

sql_params_converter = sqlparams.SQLParams('named', 'qmark')


class CursorWrapper:
    def __init__(self, cursor):
        self._cursor = cursor

        self.statement = None

    def execute(self, query, parameters=None):
        """
        :param self: django's cursor
        :param query: SQL
        :param parameters: SQL parameters
        :return:
        """
        if isinstance(parameters, dict):
            # convert sql and parameters
            _query, _parameters = sql_params_converter.format(query, parameters)

            logger.debug(
                'SQL (%s), parameters(%s) has been converted to SQL(%s), parameters(%s)',
                query, parameters, _query, _parameters)

            query, parameters = (_query, _parameters)
        else:
            # change paramstyle 'format' to 'qmark'
            query = query.replace('%s', '?')

        # record last query
        self.statement = query

        # call jaydebeapi
        self._cursor.cursor.execute(query, parameters)

    def __getattr__(self, item):
        return getattr(self._cursor, item)
