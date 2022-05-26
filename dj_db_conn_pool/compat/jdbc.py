def patch_all():
    patch_converters()


def patch_converters():
    """
    patch jaydebeapi's converters
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
