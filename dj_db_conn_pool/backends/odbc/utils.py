# -*- coding: utf-8 -*-

class CursorWrapper:
    def __init__(self, cursor):
        self._cursor = cursor

        self.statement = None

    def __getattr__(self, item):
        return getattr(self._cursor, item)
