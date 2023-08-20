import jpype


def patch_all():
    patch_converters()


def patch_converters():
    """
    patch jpype's jdbc converters
    """

    def to_python(value):
        return value._py()

    def to_number(value):
        string = str(value.toString())

        if value.scale() > 0:
            return float(string)

        return int(string)

    @jpype.onJVMStart
    def register_converters():
        from dj_db_conn_pool.backends.jdbc import jdbc_type_converters

        jdbc_type_converters[jpype.java.lang.String] = str
        jdbc_type_converters[jpype.java.sql.Date] = to_python
        jdbc_type_converters[jpype.java.sql.Time] = to_python
        jdbc_type_converters[jpype.java.sql.Timestamp] = to_python
        jdbc_type_converters[jpype.java.math.BigDecimal] = to_number
        jdbc_type_converters[jpype.JArray(jpype.types.JByte)] = bytes
        # jdbc_type_converters[type(None)] = lambda v: v
