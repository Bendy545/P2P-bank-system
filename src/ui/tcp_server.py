import socket
import threading
import time

class TCPServer:
    def __init__(self, app, client_timeout_sec=10):
        self.app = app
        self.client_timeout_sec = float(client_timeout_sec)

    def start(self, host="0.0.0.0"):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host, self.app.listen_port))
            server.listen(50)
            print(f"Listening on {host}:{self.app.listen_port} (bank code {self.app.my_bank_code})")

            while True:
                client_socket, address = server.accept()
                t = threading.Thread(target=self._handle_client, args=(client_socket, address), daemon=True)
                t.start()
        finally:
            try:
                server.close()
            except Exception:
                pass

    def _handle_client(self, client_socket, address):
        client_ip, client_port = address[0], address[1]
        client_socket.settimeout(self.client_timeout_sec)

        buf = b""
        last_activity = time.time()

        try:
            while True:
                if time.time() - last_activity > self.client_timeout_sec:
                    break

                try:
                    chunk = client_socket.recv(4096)
                except socket.timeout:
                    break

                if not chunk:
                    break

                last_activity = time.time()
                buf += chunk

                while b"\n" in buf:
                    line_bytes, buf = buf.split(b"\n", 1)
                    line = line_bytes.decode("utf-8", errors="replace").strip()
                    if not line:
                        continue

                    cmd_code = None
                    try:
                        cmd_code = line.split()[0].upper()
                    except Exception:
                        pass

                    if getattr(self.app, "logger", None):
                        self.app.logger.write_log(
                            level_name="INFO",
                            event_type="cmd_in",
                            message="Request received",
                            client_ip=client_ip,
                            client_port=client_port,
                            command=cmd_code,
                            request_raw=line
                        )

                    response = self.app.dispatcher.dispatch(line, self.app)

                    if getattr(self.app, "logger", None):
                        level = "INFO"
                        event_type = "cmd_out"
                        msg = "Response sent"

                        if response.startswith("ER"):
                            level = "ERROR"
                            event_type = "cmd_error"
                            msg = response

                        self.app.logger.write_log(
                            level_name=level,
                            event_type=event_type,
                            message=msg,
                            client_ip=client_ip,
                            client_port=client_port,
                            command=cmd_code,
                            request_raw=line,
                            response_raw=response
                        )

                    out = (response.strip() + "\n").encode("utf-8")
                    client_socket.sendall(out)

        finally:
            try:
                client_socket.close()
            except Exception:
                pass