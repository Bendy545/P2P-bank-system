from src.database.config_load import load_config
from src.database.database import Database

if __name__ == '__main__':
    config = load_config("config.json")

    db = Database(config)

    db.get_connection()

    print("connected")

    db.close()