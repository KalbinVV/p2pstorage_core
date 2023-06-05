from dataclasses import dataclass
import socket


@dataclass(frozen=True)
class Host:
    host_name: str
    host_socket: socket.socket

    def __repr__(self):
        return f'Host(host_name={self.host_name})'
