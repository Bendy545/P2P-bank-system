import re

MAX_AMOUNT = 9223372036854775807

_IP_RE = re.compile(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$")
_ACCOUNT_RE = re.compile(r"^(\d{5})\/(\d{1,3}(\.\d{1,3}){3})$")

class ParseError(Exception):
    pass

class ForeignBankError(Exception):
    pass

def _validate_ipv4(ip):
    m = _IP_RE.match(ip)
    if not m:
        raise ParseError("Invalid IP address.")

    parts = [int(x) for x in m.groups()]
    for p in parts:
        if p < 0 or p > 255:
            raise ParseError("Invalid IP address.")

    return ip

def parse_account_ref(s):
    m = _ACCOUNT_RE.match(s.strip())
    if not m:
        raise ParseError("Invalid account number.")

    acc = int(m.group(1))
    ip = m.group(2)
    if acc < 10000 or acc > 99999:
        raise ParseError("Invalid account number.")
    _validate_ipv4(ip)
    return acc, ip

def parse_amount(s):
    s = s.strip()
    if not s.isdigit():
        raise ParseError("Account number a amount are in invalid format.")
    n = int(s)
    if n < 0 or n > MAX_AMOUNT:
        raise ParseError("Amount is out of range")
    return n

def parse_line(raw_line):
    line = raw_line.strip()
    if not line:
        raise ParseError("Invalid Command.")

    parts = line.split()
    code = parts[0].upper()

    if code in ("BC", "AC", "BA", "BN"):
        if len(parts) != 1:
            raise ParseError("Invalid Command format.")
        return code, None, None

    if code in ("AB", "AR"):
        if len(parts) != 2:
            raise ParseError("Invalid Command format.")
        return code, parts[1], None

    if code in ("AD", "AW"):
        if len(parts) != 3:
            raise ParseError("Invalid Command format.")
        return code, parts[1], parts[2]

    raise ParseError("Unknown command.")