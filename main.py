from my_lib.my_library.config.json_config import load_json_config, get_int
from my_lib.my_library.util.ip_detect import detect_local_ipv4

from src.database.database import Database
from src.database.dao.accounts import Account
from src.database.dao.log import Log
from src.app.app import App
from src.ui.tcp_server import TCPServer

if __name__ == "__main__":
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

    app = App(
        account_dao=account_dao,
        my_bank_code=my_bank_code,
        listen_port=listen_port,
        remote_port=remote_port,
        cmd_timeout_sec=cmd_timeout,
        logger=logger
    )

    server = TCPServer(app, client_timeout_sec=client_timeout)
    server.start(listen_host)