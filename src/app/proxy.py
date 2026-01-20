import socket

class ProxyError(Exception):
    pass

class ProxyClient:
    MAX_RESPONSE_SIZE = 8192

    def __init__(self, remote_port, timeout_sec=5):
        self.remote_port = int(remote_port)
        self.timeout_sec = float(timeout_sec)

    def forward(self, target_ip, raw_line):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(self.timeout_sec)
            s.connect((target_ip, self.remote_port))

            data = (raw_line.strip() + "\n").encode("utf-8")
            s.sendall(data)

            buf = b""
            while b"\n" not in buf:
                chunk = s.recv(4096)
                if not chunk:
                    break

                buf += chunk
                if len(buf) > self.MAX_RESPONSE_SIZE:
                    raise ProxyError("Response too large from remote bank")

            if b"\n" not in buf:
                if buf:
                    raise ProxyError("Incomplete response from remote bank")
                else:
                    raise ProxyError("Empty response from remote bank")

            line = buf.split(b"\n", 1)[0].decode("utf-8", errors="replace")

            return line

        except socket.timeout as e:
            raise ProxyError("Proxy timeout") from e
        except Exception as e:
            raise ProxyError("Proxy connection error") from e
        finally:
            try:
                s.close()
            except Exception:
                pass