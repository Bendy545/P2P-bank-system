# src/ui/tcp_server_worker.py
import socket

from src.database.database import Database
from src.database.dao.accounts import Account
from src.database.dao.log import Log
from src.app.app import App

def _iter_lines(sock, buffer_size=4096):
    buffer = b""
    while True:
        chunk = sock.recv(buffer_size)
        if not chunk:
            return
        buffer += chunk

        if len(buffer) > 1024:
            raise Exception("Line too long")

        while True:
            nl = buffer.find(b"\n")
            if nl == -1:
                break
            line_bytes = buffer[:nl]
            buffer = buffer[nl + 1:]
            yield line_bytes.decode("utf-8", errors="replace").strip()

def handle_client_process(client_socket, address, cfg, runtime, client_timeout_sec):
    db = Database(cfg)
    account_dao = Account(db)
    logger = Log(db)

    app = App( account_dao=account_dao, my_bank_code=runtime["my_bank_code"], listen_port=runtime["listen_port"], remote_port=runtime["remote_port"], cmd_timeout_sec=runtime["cmd_timeout_sec"], logger=logger)

    client_ip, client_port = address[0], address[1]
    client_socket.settimeout(float(client_timeout_sec))

    try:
        for line in _iter_lines(client_socket):
            if not line:
                continue

            command_code = (line.split()[0].upper() if line.split() else None)

            if getattr(app, "logger", None):
                app.logger.write_log( level_name="INFO", event_type="cmd_in", message="Request received", client_ip=client_ip, client_port=client_port, command=command_code, request_raw=line)

            response = app.dispatcher.dispatch(line, app)

            if getattr(app, "logger", None):
                level = "ERROR" if response.startswith("ER") else "INFO"
                event_type = "cmd_error" if response.startswith("ER") else "cmd_out"
                message = response if response.startswith("ER") else "Response sent"
                app.logger.write_log( level_name=level, event_type=event_type, message=message, client_ip=client_ip, client_port=client_port, command=command_code, request_raw=line, response_raw=response)

            client_socket.sendall((response.strip() + "\n").encode("utf-8"))

    except socket.timeout:
        pass
    finally:
        try:
            client_socket.close()
        except Exception:
            pass
        try:
            db.close()
        except Exception:
            pass
