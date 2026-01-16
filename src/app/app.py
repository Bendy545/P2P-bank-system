from ip_detect import detect_local_ipv4
from dispatcher import Dispatcher
from src.database.dao.accounts import Account
from src.database.database import Database
from src.database.config_load import load_config

class App:
    def __init__(self, account_dao, my_bank_code=None):
        self.account_dao = account_dao
        self.my_bank_code = my_bank_code or detect_local_ipv4()
        self.dispatcher = Dispatcher(self)


if __name__ == "__main__":
    config = load_config("config.json")
    database = Database(config)
    account_dao = Account(database)
    app = App(account_dao)

    print(app.dispatcher.dispatch("BC"))
    print(app.dispatcher.dispatch("AC"))