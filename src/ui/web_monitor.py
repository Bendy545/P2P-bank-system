import os
import threading

from flask import Flask, render_template, jsonify, abort
import sys

def _build_status(app_obj, server_obj, database):
    my_ip = getattr(app_obj, "my_bank_code", None)
    listen_port = getattr(app_obj, "listen_port", None)
    remote_port = getattr(app_obj, "remote_port", None)
    cmd_timeout_sec = getattr(app_obj, "cmd_timeout_sec", None)

    try:
        client_count = app_obj.account_dao.bank_number_of_clients(app_obj.my_bank_code)
    except Exception as e:
        client_count = f"error: {e}"

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
            "server_running": server_running,
            "db_backend": database
        }

def create_monitor_app(app_obj, server_obj, database):
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    flask_app = Flask(__name__, template_folder=template_dir)

    @flask_app.route('/')
    def index():
        print("Monitor: index requested", file=sys.stderr, flush=True)
        status = _build_status(app_obj, server_obj, database)
        return render_template("monitor.html", status=status)

    @flask_app.route('/api/status', methods=['GET'])
    def api_status():
        status = _build_status(app_obj, server_obj)
        return jsonify(status)

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

