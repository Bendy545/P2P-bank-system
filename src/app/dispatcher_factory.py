from my_lib.my_library.command.dispatcher import Dispatcher
from my_lib.my_library.command.response import err

from src.app.parse import ParseError, ForeignBankError, parse_line
from src.database.dao.errors import AccountNotFound, NotEnoughFunds, AccountNotEmpty, DuplicateAccount
from src.app.proxy import ProxyError

def error_mapper(e):
    if isinstance(e, ParseError):
        return "ER " + str(e)
    if isinstance(e, ProxyError):
        return "ER Error when communicating with another bank."
    if isinstance(e, AccountNotFound):
        return "ER Account not found."
    if isinstance(e, NotEnoughFunds):
        return "ER Not enough funds."
    if isinstance(e, AccountNotEmpty):
        return "ER Account not empty."
    if isinstance(e, DuplicateAccount):
        return "ER Unavailable to create a new account."

    if isinstance(e, ForeignBankError):
        return "ER Foreign bank."

    return None

def build_dispatcher(commands_dict):
    return Dispatcher(
        parse_line_func=parse_line,
        commands_dict=commands_dict,
        error_mapper=error_mapper
    )
