from src.data.config_load import load_config
from src.data.database import Database

if __name__ == '__main__':
    config = load_config("config.json")

    db = Database(config)

    print("pripojeno")

    db.close()