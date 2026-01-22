import os
from flask import Flask, render_template
import sys

def create_monitor_app():
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    flask_app = Flask(__name__, template_folder=template_dir)

    @flask_app.route('/')
    def index():
        print("Monitor: index requested", file=sys.stderr, flush=True)

        status = {
            "my_bank_code": "127.0.0.1",
            "listen_port": 9000,
            "remote_port": 9001,
            "cmd_timeout_sec": 10,
            "client_count": 0,
            "server_running": True,
            "db_backend": "mysql"
        }

        return render_template("monitor.html", status=status)

    return flask_app

