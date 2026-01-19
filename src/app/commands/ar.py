from my_lib.my_library.command.base import Command
from src.app.parse import ForeignBankError
from src.app.parse import parse_account_ref, ParseError

class ARCommand(Command):
    def execute(self, app, raw_line, arg1, arg2):
        account_no, bank_code = parse_account_ref(arg1)

        if bank_code != app.my_bank_code:
            raise ForeignBankError()

        app.account_dao.delete_account(account_no, bank_code)
        return ("AR", None)