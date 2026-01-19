import sqlite3
import threading

class SQLiteDatabase:
    def __init__(self, path="p2p_bank.db"):
        self._path = path
        self._local = threading.local()

    def connect(self):
        conn = self.get_connection()
        self._init_schema(conn)
        return True

    def get_connection(self):
        conn = getattr(self._local, "conn", None)
        if conn is None:
            raw = sqlite3.connect(self._path, timeout=5, check_same_thread=False)
            raw.execute("PRAGMA foreign_keys = ON;")
            conn = _SQLiteConnectionAdapter(raw)
            self._local.conn = conn
        return conn

    def close(self):
        conn = getattr(self._local, "conn", None)
        if conn:
            conn.close()
            self._local.conn = None

    def _init_schema(self, conn):
        schema = """
        CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_no INTEGER NOT NULL,
            bank_code TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(bank_code, account_no)
        );

        CREATE INDEX IF NOT EXISTS ix_accounts_bank_code ON accounts(bank_code);

        CREATE TABLE IF NOT EXISTS account_tx(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            tx_type TEXT NOT NULL,
            amount INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(account_id) REFERENCES accounts(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS node_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            level_name TEXT NOT NULL DEFAULT 'INFO',
            event_type TEXT NOT NULL,
            client_ip TEXT,
            client_port INTEGER,
            command TEXT,
            account_no INTEGER,
            bank_code TEXT,
            request_raw TEXT,
            response_raw TEXT,
            message TEXT NOT NULL
        );

        CREATE TRIGGER IF NOT EXISTS trg_accounts_updated_at
        AFTER UPDATE ON accounts
        FOR EACH ROW
        BEGIN
            UPDATE accounts SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
        END;
        """
        cur = conn.cursor()
        try:
            cur._raw.executescript(schema)
            conn.commit()
        finally:
            cur.close()


class _SQLiteConnectionAdapter:
    def __init__(self, raw_conn):
        self._raw = raw_conn

    def cursor(self):
        return _SQLiteCursorAdapter(self._raw.cursor())

    def commit(self):
        return self._raw.commit()

    def rollback(self):
        return self._raw.rollback()

    def close(self):
        return self._raw.close()


class _SQLiteCursorAdapter:
    def __init__(self, raw_cursor):
        self._raw = raw_cursor

    def execute(self, sql, params=None):
        sql2 = self._translate_sql(sql)
        if params is None:
            return self._raw.execute(sql2)
        return self._raw.execute(sql2, params)

    def fetchone(self):
        return self._raw.fetchone()

    def fetchall(self):
        return self._raw.fetchall()

    def close(self):
        return self._raw.close()

    def _translate_sql(self, sql):
        s = sql.replace("%s", "?")
        s = s.replace(" FOR UPDATE", "")
        return s
