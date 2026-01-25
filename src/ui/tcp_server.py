import socket
from multiprocessing import Process

from src.ui.tcp_server_worker import handle_client_process

class TCPServer:
    def __init__(self, cfg, runtime, client_timeout_sec=10):
        self.cfg = cfg
        self.runtime = runtime
        self.client_timeout_sec = float(client_timeout_sec)
        self._server_socket = None
        self._running = False

    def start(self, host="0.0.0.0"):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket = server

        try:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host, self.runtime["listen_port"]))
            server.listen(50)
            server.settimeout(1.0)

            self._running = True
            print(f"Listening on {host}:{self.runtime['listen_port']} (bank code {self.runtime['my_bank_code']})", flush=True)

            while self._running:
                try:
                    client_socket, address = server.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break

                p = Process(target=handle_client_process,args=(client_socket, address, self.cfg, self.runtime, self.client_timeout_sec))
                p.daemon = True
                p.start()

                client_socket.close()

        finally:
            self._running = False
            try:
                server.close()
            except Exception:
                pass

    def stop(self):
        self._running = False
        try:
            if self._server_socket:
                self._server_socket.close()
        except Exception:
            pass

    def is_running(self):
        return self._running