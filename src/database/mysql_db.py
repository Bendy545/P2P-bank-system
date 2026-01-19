import mysql.connector
import threading

class MySQLDatabase:
    def __init__(self, config):
        self._config = config
        self._local = threading.local()

    def connect(self):
        return True

    def get_connection(self):
        conn = getattr(self._local, "conn", None)
        if conn is None or not conn.is_connected():
            conn = mysql.connector.connect(
                host=self._config["host"],
                user=self._config["user"],
                password=self._config["password"],
                database=self._config["database"],
                autocommit=False,
                connection_timeout=self._config.get("db_connect_timeout", 5),
            )
            self._local.conn = conn
        return conn

    def close(self):
        conn = getattr(self._local, "conn", None)
        if conn:
            conn.close()
            self._local.conn = None
