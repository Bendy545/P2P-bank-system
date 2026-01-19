import random
from my_lib.my_library.command.base import Command
from src.database.dao.errors import DuplicateAccount

class ACCommand(Command):
    def execute(self, app, raw_line, arg1, arg2):
        for _ in range(30):
            account_no = random.randint(10000, 99999)
            try:
                ref = app.account_dao.create_account(app.my_bank_code, account_no)
                return ("AC", ref)
            except DuplicateAccount:
                continue
        raise Exception("Not available to create a new account")
