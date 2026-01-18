from src.app.dispatcher_factory import build_dispatcher
from src.app.proxy import ProxyClient

from src.app.commands.bc import BCCommand
from src.app.commands.ac import ACCommand
from src.app.commands.ab import ABCommand
from src.app.commands.ad import ADCommand
from src.app.commands.aw import AWCommand
from src.app.commands.ar import ARCommand
from src.app.commands.ba import BACommand
from src.app.commands.bn import BNCommand

class App:
    def __init__(self, account_dao, my_bank_code, listen_port, remote_port, cmd_timeout_sec=5, logger=None):
        self.account_dao = account_dao
        self.my_bank_code = my_bank_code
        self.listen_port = int(listen_port)
        self.remote_port = int(remote_port)
        self.cmd_timeout_sec = float(cmd_timeout_sec)
        self.logger = logger
        self.proxy_client = ProxyClient(remote_port=self.remote_port, timeout_sec=self.cmd_timeout_sec)

        commands = {
            "BC": BCCommand(),
            "AC": ACCommand(),
            "AB": ABCommand(),
            "AD": ADCommand(),
            "AW": AWCommand(),
            "AR": ARCommand(),
            "BA": BACommand(),
            "BN": BNCommand(),
        }

        self.dispatcher = build_dispatcher(commands)