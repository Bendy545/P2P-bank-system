from my_lib.my_library.command.base import Command

class BNCommand(Command):
    def execute(self, app, raw_line, arg1, arg2):
        total_clients = app.account_dao.bank_number_of_clients(app.my_bank_code)
        return ("BN", total_clients)