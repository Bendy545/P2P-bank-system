from parse import parse_line, ParseError
from response import ok, err

from src.database.dao.errors import AccountNotFound, NotEnoughFunds, AccountNotEmpty, DuplicateAccount

from commands.bc import BCCommand
from commands.ac import ACCommand
from commands.ab import ABCommand

class Dispatcher:
    def __init__(self, app):
        self.app = app
        self.commands = {
            "BC": BCCommand(),
            "AC": ACCommand(),
            "AB": ABCommand(),
        }

    def dispatch(self, raw_line):
        try:
            code, arg1, arg2 = parse_line(raw_line)
            cmd = self.commands.get(code)
            if not cmd:
                return err("Unknown command.")

            out_code, payload = cmd.execute(self.app, raw_line, arg1, arg2)
            return ok(out_code, payload)

        except ParseError as e:
            return err(str(e))

        except AccountNotFound:
            return err("Account not found.")

        except NotEnoughFunds:
            return err("Not enough funds.")

        except AccountNotEmpty:
            return err("Account not empty.")

        except DuplicateAccount:
            return err("Unavailable to create a new account.")

        except Exception:
            return err("Error occurred in application.")
