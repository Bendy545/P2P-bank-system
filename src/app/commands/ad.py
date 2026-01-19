from my_lib.my_library.command.base import Command
from src.app.parse import parse_account_ref, parse_amount
from src.app.proxy import ProxyError

class ADCommand(Command):
    def execute(self, app, raw_line, arg1, arg2):
        account_no, bank_code = parse_account_ref(arg1)
        amount = parse_amount(arg2)

        if bank_code != app.my_bank_code:
            resp = app.proxy_client.forward(bank_code, raw_line)
            return ("RAW", resp)

        app.account_dao.deposit(account_no, bank_code, amount)
        return ("AD", None)