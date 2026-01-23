import os
import threading

from flask import Flask, render_template, jsonify, abort
import sys

def _build_status(app_obj, server_obj):
    server_running = "unknown"
    try:
        if hasattr(server_obj, "is_running") and callable(server_obj.is_running):
            server_running = bool(server_obj.is_running())
    except Exception:
        server_running = "error"

    return {
            "my_bank_code": "127.0.0.1",
            "listen_port": 9000,
            "remote_port": 9001,
            "cmd_timeout_sec": 10,
            "client_count": 0,
            "server_running": server_running,
            "db_backend": "mysql"
        }

def create_monitor_app(app_obj, server_obj):
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    flask_app = Flask(__name__, template_folder=template_dir)

    @flask_app.route('/')
    def index():
        print("Monitor: index requested", file=sys.stderr, flush=True)
        status = _build_status(app_obj, server_obj)
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

