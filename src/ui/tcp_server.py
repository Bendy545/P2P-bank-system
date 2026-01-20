import socket
import threading
import multiprocessing
from multiprocessing import Process

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
                p = Process(target=self._handle_client, args=(client_socket, address))
                p.daemon = True
                p.start()

                client_socket.close()
        finally:
            try:
                server.close()
            except Exception:
                pass

    def _iter_lines(self, sock, buffer_size=4096):
        buffer = b""

        while True:
            chunk = sock.recv(buffer_size)
            if not chunk:
                return
            buffer+= chunk

            if len(buffer) > 1024:
                raise Exception("Line too long")

            while True:
                new_line = buffer.find(b"\n")
                if new_line == -1:
                    break
                line_bytes = buffer[:new_line]
                buffer = buffer[new_line + 1:]
                yield line_bytes.decode("utf-8", errors="replace").strip()

    def _handle_client(self, client_socket, address):
        client_ip, client_port = address[0], address[1]
        client_socket.settimeout(self.client_timeout_sec)

        try:
            for line in self._iter_lines(client_socket):
                if not line:
                    continue

                command_code = (line.split()[0].upper() if line.split() else None)

                if getattr(self.app, "logger", None):
                    self.app.logger.write_log(level_name="INFO", event_type="cmd_in", message="Request received", client_ip=client_ip, client_port=client_port, command=command_code, request_raw=line)

                response = self.app.dispatcher.dispatch(line, self.app)

                if getattr(self.app, "logger", None):
                    level = "ERROR" if response.startswith("ER") else "INFO"
                    event_type = "cmd_error" if response.startswith("ER") else "cmd_out"
                    message = response if response.startswith("ER") else "Response sent"
                    self.app.logger.write_log(level_name=level,event_type=event_type, message=message, client_ip=client_ip, client_port=client_port, command=command_code, request_raw=line, response_raw=response)

                client_socket.sendall((response.strip() + "\n").encode("utf-8"))

        except socket.timeout:
            pass
        finally:
            try:
                client_socket.close()
            except Exception:
                pass