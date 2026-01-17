from src.app.commands.base import Command

class BCCommand(Command):
    def execute(self, app, raw_line, arg1, arg2):
        return ("BC", app.my_bank_code)