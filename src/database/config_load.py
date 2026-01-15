import json
import os

class ConfigError(Exception):
    pass

def load_config(file_path="db/config.json"):
    if not os.path.exists(file_path):
        raise ConfigError("Config File Not Found")

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            raise ConfigError("Invalid Config File")

    required_keys = ["host", "user", "password", "database"]
    for key in required_keys:
        if key not in config:
            raise ConfigError(f"Missing required parameter '{key}' in config file.")

    for key in ["user", "password", "host", "database"]:
        if not isinstance(config[key], str) or not config[key].strip():
            raise ConfigError(f"{key} must not be a non-empty string.")

    return config