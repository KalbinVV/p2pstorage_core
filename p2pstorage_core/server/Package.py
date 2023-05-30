from enum import Enum


class PackageType(Enum):
    HOST_CONNECTED = 1,
    HOST_DISCONNECTED = 2,
    SUCCESSFUL_CONNECT_RESPONSE = 3
