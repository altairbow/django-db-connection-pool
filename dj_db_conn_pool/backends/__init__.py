class BaseDatabaseWrapper:
    def get_new_connection(self, conn_params):
        return super(BaseDatabaseWrapper, self).get_new_connection(conn_params)

    def close(self, *args, **kwargs):
        return super(BaseDatabaseWrapper, self).close(*args, **kwargs)
