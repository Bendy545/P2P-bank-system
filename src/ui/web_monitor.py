import os
import threading
from src.database.database import Database
from src.database.dao.log import Log
from src.app.log_service import LogService
from src.database.dao.accounts import Account

from flask import Flask, render_template, jsonify, abort
import sys

def _build_status(app_obj, server_obj, database, account_dao):
    my_ip = getattr(app_obj, "my_bank_code", None)
    listen_port = getattr(app_obj, "listen_port", None)
    remote_port = getattr(app_obj, "remote_port", None)
    cmd_timeout_sec = getattr(app_obj, "cmd_timeout_sec", None)

    try:
        client_count = account_dao.bank_number_of_clients(app_obj.my_bank_code)
    except Exception as e:
        client_count = f"error: {e}"

    try:
        bank_total = account_dao.bank_total_amount(app_obj.my_bank_code)
    except Exception as e:
        bank_total = f"error: {e}"

    server_running = "unknown"
    try:
        if hasattr(server_obj, "is_running") and callable(server_obj.is_running):
            server_running = bool(server_obj.is_running())
    except Exception:
        server_running = "error"

    return {
            "my_bank_code": my_ip,
            "listen_port": listen_port,
            "remote_port": remote_port,
            "cmd_timeout_sec": cmd_timeout_sec,
            "client_count": client_count,
            "bank_total": bank_total,
            "server_running": server_running,
            "db_backend": database
        }

def create_monitor_app(app_obj, server_obj, database, cfg):
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    flask_app = Flask(__name__, template_folder=template_dir, static_folder=os.path.join(os.path.dirname(__file__), "static"))
    monitor_db = Database(cfg)
    monitor_log_dao = Log(monitor_db)
    log_service = LogService(monitor_log_dao)
    monitor_account_dao = Account(monitor_db)


    @flask_app.route('/')
    def index():
        print("Monitor: index requested", file=sys.stderr, flush=True)
        status = _build_status(app_obj, server_obj, database, monitor_account_dao)
        return render_template("monitor.html", status=status)

    @flask_app.route('/api/status', methods=['GET'])
    def api_status():
        status = _build_status(app_obj, server_obj, database, monitor_account_dao)
        return jsonify(status)

    @flask_app.route("/api/logs", methods=['GET'])
    def api_logs():
        try:
            logs = log_service.get_last_logs(limit=20)
            return jsonify(logs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @flask_app.route('/shutdown', methods=['POST'])
    def shutdown():
        print("Monitor: shutdown requested", file=sys.stderr, flush=True)
        try:
            threading.Thread(target=server_obj.stop, daemon=True).start()
        except Exception as e:
            print("Monitor: shutdown error:", e, file=sys.stderr, flush=True)
            abort(500)
        return "Shutdown initiated", 200

    return flask_app