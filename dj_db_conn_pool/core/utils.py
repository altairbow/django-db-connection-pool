import logging
import sqlparams

logger = logging.getLogger(__name__)


class CursorWrapper:
    def __init__(self, cursor, style, sql_converter):
        self._cursor = cursor

        self._sql_params_converter = sqlparams.SQLParams('named', style, True, True)

        self._sql_converter = sql_converter

        self._statement = None

    def execute(self, query, parameters=None):
        if isinstance(parameters, dict):
            _query, _parameters = self._sql_params_converter.format(query, parameters)
        else:
            _query, _parameters = self._sql_converter(query), parameters

        if query != _query:
            logger.debug(
                'SQL (%s), parameters(%s) has been converted to SQL(%s), parameters(%s)',
                query, parameters, _query, _parameters
            )

        query, parameters = _query, _parameters

        try:
            cursor = self._cursor.cursor
        except AttributeError:
            cursor = self._cursor

        self._statement = query

        return cursor.execute(query, parameters or [])

    def __getattr__(self, attr):
        try:
            return getattr(self._cursor, attr)
        except AttributeError:
            if attr == 'statement':
                return self._statement
            raise
