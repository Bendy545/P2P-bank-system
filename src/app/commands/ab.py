from src.app.commands.base import Command
from src.app.parse import parse_account_ref

class ABCommand(Command):
    def execute(self, app, raw_line, arg1, arg2):
        account_no, bank_code = parse_account_ref(arg1)
        balance = app.account_dao.get_balance(account_no, bank_code)
        return ("AB", str(balance))