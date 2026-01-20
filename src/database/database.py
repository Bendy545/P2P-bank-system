class Database:
    def __init__(self, config):
        self._config = config
        self._impl = None
        self._backend = None

        self._select_strategy()

    def _select_strategy(self):
        try:
            from src.database.mysql_db import MySQLDatabase
            impl = MySQLDatabase(self._config)

            impl.connect()

            self._impl = impl
            self._backend = "mysql"
            print("DB Strategy: MySQL")
            return
        except Exception as e:
            print(f"DB Strategy: MySQL unavailable ({e}) -> fallback to SQLite")

        from src.database.sqlite_db import SQLiteDatabase
        path = self._config.get("sqlite_path", "p2p_bank.db")
        impl = SQLiteDatabase(path)
        impl.connect()
        self._impl = impl
        self._backend = "sqlite"
        print("DB Strategy: SQLite")

    def get_connection(self):
        return self._impl.get_connection()

    def close(self):
        return self._impl.close()

    def backend_name(self):
        return self._backend