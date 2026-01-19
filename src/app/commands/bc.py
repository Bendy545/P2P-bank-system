from my_lib.my_library.command.base import Command

class BCCommand(Command):
    def execute(self, app, raw_line, arg1, arg2):
        return ("BC", app.my_bank_code)