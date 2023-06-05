from dataclasses import dataclass
import socket
from typing import NamedTuple

from p2pstorage_core.helper_classes.SocketAddress import SocketAddress


@dataclass(frozen=True)
class Host:
    host_name: str
    host_socket: socket.socket

    def __repr__(self):
        return f'Host(host_name={self.host_name}, addr={self.host_socket.getpeername()})'


class HostInfo(NamedTuple):
    host_name: str
    host_addr: SocketAddress
