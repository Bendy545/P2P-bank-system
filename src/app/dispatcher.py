from src.app.commands.ad import ADCommand
from src.app.commands.aw import AWCommand
from src.app.parse import parse_line, ParseError, ForeignBankError
from src.app.response import ok, err
from src.app.commands.ar import ARCommand
from src.app.commands.ba import BACommand
from src.app.commands.bn import BNCommand

from src.database.dao.errors import AccountNotFound, NotEnoughFunds, AccountNotEmpty, DuplicateAccount

from src.app.commands.bc import BCCommand
from src.app.commands.ac import ACCommand
from src.app.commands.ab import ABCommand
from src.app.commands.ba import BACommand
from src.app.commands.bn import BNCommand

class Dispatcher:
    def __init__(self, app):
        self.app = app
        self.commands = {
            "BC": BCCommand(),
            "AC": ACCommand(),
            "AB": ABCommand(),
            "BA": BACommand(),
            "BN": BNCommand(),
            "AR": ARCommand(),
            "AD": ADCommand(),
            "AW": AWCommand(),
        }

    def dispatch(self, raw_line):
        try:
            code, arg1, arg2 = parse_line(raw_line)
            cmd = self.commands.get(code)
            if not cmd:
                return err("Unknown command.")

            out_code, payload = cmd.execute(self.app, raw_line, arg1, arg2)

            if out_code == "RAW":
                return payload

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

        except ForeignBankError:
            return err("Foreign bank.")

        except Exception:
            return err("Error occurred in application.")
