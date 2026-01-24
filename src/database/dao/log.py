class Log:
    def __init__(self, db):
        self.db = db

    def write_log(self, level_name, event_type, message, client_ip=None, client_port=None, command=None, account_no=None, bank_code=None, request_raw=None, response_raw=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO node_log (level_name, event_type, client_ip, client_port, command, account_no, bank_code, request_raw, response_raw, message)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                level_name,
                event_type,
                client_ip,
                client_port,
                command,
                account_no,
                bank_code,
                request_raw,
                response_raw,
                message
            ))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def last_logs(self, limit: int = 50):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT created_at, level_name, event_type, command, account_no, bank_code, message
                FROM node_log ORDER BY created_at DESC LIMIT %s
                """, (limit,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.commit()
