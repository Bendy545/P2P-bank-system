class LogService:
    def __init__(self, log_dao):
        self._log_dao = log_dao

    def get_last_logs(self, limit: int = 20):
        rows = self._log_dao.last_logs(limit)

        logs = []
        for r in rows:
            logs.append({
                "created_at": r[0],
                "level": r[1],
                "event_type": r[2],
                "command": r[3],
                "account_no": r[4],
                "bank_code": r[5],
                "message": r[6],
            })

        return logs
