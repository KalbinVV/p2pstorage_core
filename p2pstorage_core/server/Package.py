from enum import Enum

from p2pstorage_core.server import StreamConfiguration


class PackageType(Enum):
    HOST_CONNECT_REQUEST = 1,
    HOST_SUCCESSFUL_CONNECT_RESPONSE = 2,


class Package:
    def __init__(self, data: bytes):
        self.__data = data

    def to_json(self) -> str:
        return self.__data.decode(StreamConfiguration.ENCODING_FORMAT)
