import jaydebeapi
from datetime import datetime


def patch_all():
    patch_converters()


def patch_converters():
    """
    patch jaydebeapi's converters
    """
    def to_number(rs, col):
        java_obj = rs.getBigDecimal(col)

        py_str = rs.getString(col)

        if java_obj.scale() > 0:
            return float(py_str)

        return int(py_str)

    def to_str(rs, col):
        return rs.getString(col)

    def to_datetime(rs, col):
        java_obj = rs.getTimestamp(col).getTime()

        time_stamp = int(str(java_obj)) // 1000

        dt = datetime.fromtimestamp(time_stamp)

        return dt

    jaydebeapi._DEFAULT_CONVERTERS.update(
        {
            'CHAR': to_str,
            'VARCHAR': to_str,
            'NUMERIC': to_number,
            'TIMESTAMP': to_datetime,
         }
    )
