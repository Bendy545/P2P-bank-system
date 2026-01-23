import multiprocessing
from threading import Thread

from my_lib.my_library.config.json_config import load_json_config, get_int
from my_lib.my_library.util.ip_detect import detect_local_ipv4

from src.database.database import Database
from src.database.dao.accounts import Account
from src.database.dao.log import Log
from src.app.app import App
from src.ui.tcp_server import TCPServer

from src.ui.web_monitor import create_monitor_app


def main():
    cfg = load_json_config("config.json", required_keys=["host", "user", "password", "database"])

    listen_host = cfg.get("listen_host", "0.0.0.0")
    listen_port = get_int(cfg, "listen_port")
    remote_port = get_int(cfg, "remote_port")
    cmd_timeout = get_int(cfg, "command_timeout_sec")
    client_timeout = get_int(cfg, "client_timeout_sec")

    my_bank_code = detect_local_ipv4()

    db = Database(cfg)
    account_dao = Account(db)
    logger = Log(db)
    database_name = db.backend_name()

    app = App(
        account_dao=account_dao,
        my_bank_code=my_bank_code,
        listen_port=listen_port,
        remote_port=remote_port,
        cmd_timeout_sec=cmd_timeout,
        logger=logger
    )

    server = TCPServer(app, client_timeout_sec=client_timeout)

    server_thread = Thread(
        target=server.start,
        args=(listen_host,),
        daemon=True
    )
    server_thread.start()

    print(f"TCP server running on {listen_host}:{listen_port}", flush=True)

    monitor_app = create_monitor_app(app, server, database_name)
    monitor_port = cfg.get("monitor_port", 5000)
    monitor_app.run(host="127.0.0.1", port=monitor_port, debug=False, use_reloader=False)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
