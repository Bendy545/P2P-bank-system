import mysql.connector
import threading

class Database:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, config):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._config = config
                cls._instance._local = threading.local()
        return cls._instance

    def _connect_if_needed(self):
        conn = getattr(self._local, "conn", None)
        if conn is None or not conn.is_connected():
            conn = mysql.connector.connect(
                host=self._config['host'],
                user=self._config['user'],
                password=self._config['password'],
                database=self._config['database'],
                autocommit=False,
                connection_timeout=self._config.get("db_connect_timeout", 5)
            )
            print("Database connection Initialized.")
            self._local.conn = conn
        return conn

    def get_connection(self):
        return self._connect_if_needed()

    def close(self):
        conn = getattr(self._local, "conn", None)
        if conn:
            conn.close()
            self._local.conn = None