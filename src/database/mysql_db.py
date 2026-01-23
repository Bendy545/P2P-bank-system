import mysql.connector
import os


class MySQLDatabase:
    def __init__(self, config):
        self._config = config
        self._connections = {}

    def connect(self):
        try:
            test_conn = mysql.connector.connect(
                host=self._config["host"],
                user=self._config["user"],
                password=self._config["password"],
                database=self._config["database"],
                autocommit=False,
                connection_timeout=self._config.get("db_connect_timeout", 5),
            )

            print(f"Connected k DB '{self._config['database']}'. Checking scheme...")
            self._ensure_schema_exists(test_conn)

            test_conn.close()
            return True

        except mysql.connector.Error as err:
            print(f"ERROR Connecting: Unable to connect to database '{self._config.get('database')}'.")
            raise err

    def _ensure_schema_exists(self, conn):
        cursor = conn.cursor()
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sql_file_path = os.path.join(current_dir, "sql", "DATABASE.sql")

            if not os.path.exists(sql_file_path):
                print(f"WARNING: file {sql_file_path} not found!")
                return

            with open(sql_file_path, 'r', encoding='utf-8') as f:
                full_script = f.read()

            commands = full_script.split(';')

            for command in commands:
                clean_command = command.strip()
                if clean_command:
                    try:
                        cursor.execute(clean_command)
                    except mysql.connector.Error as e:
                        print(f"note to command: {e}")

            conn.commit()
            print("database initialization complete.")

        except Exception as err:
            print(f"Error executing sql script: {err}")
            conn.rollback()
            raise
        finally:
            cursor.close()

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