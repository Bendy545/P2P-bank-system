from my_lib.my_library.command.base import Command

class BACommand(Command):
    def execute(self, app, raw_line, arg1, arg2):
        total_amount = app.account_dao.bank_total_amount(app.my_bank_code)
        return ("BA", str(total_amount))
