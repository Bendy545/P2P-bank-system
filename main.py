from src.database.config_load import load_config
from src.database.database import Database
from src.database.dao.accounts import Account

from src.app.app import App
from src.ui.tcp_server import TCPServer

if __name__ == "__main__":
    config = load_config("config.json")

    listen_port = config.get("listen_port")
    remote_port = config.get("remote_port")
    cmd_timeout = config.get("command_timeout_sec")
    client_timeout = config.get("client_timeout_sec")

    db = Database(config)
    account_dao = Account(db)

    app = App(account_dao, listen_port=listen_port, remote_port=remote_port, cmd_timeout_sec=cmd_timeout)
    server = TCPServer(app, client_timeout_sec=client_timeout)
    server.start()