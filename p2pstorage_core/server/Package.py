from dataclasses import dataclass
from enum import Enum

from p2pstorage_core.helper_classes.SocketAddress import SocketAddress
from p2pstorage_core.server.Header import Header


class PackageType(Enum):
    HOST_CONNECTED = 1,
    HOST_DISCONNECTED = 2,
    SUCCESSFUL_CONNECT_RESPONSE = 3


@dataclass
class AbstractPackage:
    header: Header
    data: bytes
