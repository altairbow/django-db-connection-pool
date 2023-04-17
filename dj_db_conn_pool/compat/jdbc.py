import jpype
from datetime import datetime


def patch_all():
    patch_converters()


def patch_converters():
    """
    patch jpype's jdbc converters
    """
    def to_str(value):
        return str(value.toString())

    def to_number(value):
        string = str(value.toString())

        if value.scale() > 0:
            return float(string)

        return int(string)

    def to_datetime(value):
        timestamp = int(str(value.getTime())) // 1000

        return datetime.fromtimestamp(timestamp)

    @jpype.onJVMStart
    def register_converters():
        from dj_db_conn_pool.backends.jdbc import JDBC_TYPE_CONVERTERS

        JDBC_TYPE_CONVERTERS[jpype.java.lang.String] = to_str

        JDBC_TYPE_CONVERTERS[jpype.java.math.BigDecimal] = to_number

        JDBC_TYPE_CONVERTERS[jpype.java.sql.Timestamp] = to_datetime
