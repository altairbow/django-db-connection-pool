import jpype.dbapi2


class JdbcDialectMixin:
    def do_ping(self, dbapi_connection):
        try:
            return super().do_ping(dbapi_connection)
        except jpype.dbapi2.DatabaseError:
            return False
