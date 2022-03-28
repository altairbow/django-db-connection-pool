def patch_all():
    patch_converters()


def patch_converters():
    """
    ['BIT', 'TINYINT', 'SMALLINT', 'INTEGER', 'BIGINT', 'FLOAT', 'REAL', 'DOUBLE',
    'NUMERIC', 'DECIMAL', 'CHAR', 'VARCHAR', 'LONGVARCHAR', 'DATE', 'TIME', 'TIMESTAMP',
    'BINARY', 'VARBINARY', 'LONGVARBINARY', 'NULL', 'OTHER', 'JAVA_OBJECT', 'DISTINCT',
    'STRUCT', 'ARRAY', 'BLOB', 'CLOB', 'REF', 'DATALINK', 'BOOLEAN', 'ROWID', 'NCHAR',
    'NVARCHAR', 'LONGNVARCHAR', 'NCLOB', 'SQLXML', 'REF_CURSOR', 'TIME_WITH_TIMEZONE', 'TIMESTAMP_WITH_TIMEZONE']
    """
    from datetime import datetime
    import jaydebeapi

    def _to_str(rs, col):
        return str(rs.getObject(col))

    def _to_datetime(rs, col):
        java_val = rs.getTimestamp(col)

        if not java_val:
            return

        dt = datetime.strptime(
            str(java_val)[:19], '%Y-%m-%d %H:%M:%S')

        dt = dt.replace(microsecond=int(str(java_val.getNanos())[:6]))
        return dt

    jaydebeapi._DEFAULT_CONVERTERS.update(
        {
            'TIMESTAMP': _to_datetime,
            'VARCHAR': _to_str
         }
    )
