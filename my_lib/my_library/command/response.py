def ok(code, payload=None):
    if payload is None or payload == "":
        return f"{code}"
    return f"{code} {payload}"

def err(message):
    return f"ER {message}"