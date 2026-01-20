import mysql.connector
import os

class MySQLDatabase:
    def __init__(self, config):
        self._config = config
        self._connections = {}

    def connect(self):
        return True

    def get_connection(self):
        pid = os.getpid()
        conn = self._connections.get(pid)
        if conn is None or not conn.is_connected():
            conn = mysql.connector.connect(
                host=self._config["host"],
                user=self._config["user"],
                password=self._config["password"],
                database=self._config["database"],
                autocommit=False,
                connection_timeout=self._config.get("db_connect_timeout", 5),
            )
            self._connections[pid] = conn
        return conn

    def close(self):
        pid = os.getpid()
        conn = self._connections.get(pid)
        if conn:
            conn.close()
            del self._connections[pid]
