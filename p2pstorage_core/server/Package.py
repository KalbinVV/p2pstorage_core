from dataclasses import dataclass
from enum import Enum

from p2pstorage_core.helper_classes.SocketAddress import SocketAddress
from p2pstorage_core.server.Header import Header


class PackageType(Enum):
    HOST_CONNECTED = 1,
    HOST_DISCONNECTED = 2


@dataclass
class AbstractPackage:
    header: Header
    data: bytes


class HostConnectedPackage(AbstractPackage):
    def __init__(self, header: Header):
        super().__init__(header, b'')
