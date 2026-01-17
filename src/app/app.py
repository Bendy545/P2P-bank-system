from src.app.ip_detect import detect_local_ipv4
from src.app.dispatcher import Dispatcher
from src.app.proxy import ProxyClient

class App:
    def __init__(self, account_dao, listen_port, remote_port,my_bank_code=None, cmd_timeout_sec=5):
        self.account_dao = account_dao
        self.my_bank_code = my_bank_code or detect_local_ipv4()
        self.listen_port = int(listen_port)
        self.remote_port = int(remote_port)
        self.cmd_timeout_sec = float(cmd_timeout_sec)
        self.proxy_client = ProxyClient(remote_port=self.remote_port, timeout_sec=self.cmd_timeout_sec)
        self.dispatcher = Dispatcher(self)