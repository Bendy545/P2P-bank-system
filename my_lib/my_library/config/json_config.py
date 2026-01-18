import json
import os

class ConfigError(Exception):
    pass

def load_json_config(file_path, required_keys=None):
    if not os.path.exists(file_path):
        raise ConfigError("Config file not found")

    f = None
    try:
        f = open(file_path, "r", encoding="utf-8")
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            raise ConfigError("Invalid config file")
    finally:
        if f:
            f.close()

    if required_keys:
        for k in required_keys:
            if k not in config:
                raise ConfigError("Missing required parameter '" + k + "' in config file.")

    return config

def get_int(cfg, key, default=None, min_value=None, max_value=None):
    if key not in cfg:
        if default is None:
            raise ConfigError("Missing required parameter '" + key + "' in config file.")
        return default

    val = cfg[key]
    if not isinstance(val, int):
        raise ConfigError(key + " must be an integer")

    if min_value is not None and val < min_value:
        raise ConfigError(key + " is below minimum")
    if max_value is not None and val > max_value:
        raise ConfigError(key + " is above maximum")

    return val

def get_str(cfg, key, default=None):
    if key not in cfg:
        if default is None:
            raise ConfigError("Missing required parameter '" + key + "' in config file.")
        return default

    val = cfg[key]
    if not isinstance(val, str) or not val.strip():
        raise ConfigError(key + " must be a non-empty string")

    return val.strip()