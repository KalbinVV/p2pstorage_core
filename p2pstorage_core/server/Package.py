import json
from enum import IntEnum

from p2pstorage_core.server import StreamConfiguration


class PackageType(IntEnum):
    HOST_CONNECT_REQUEST = 1
    HOST_SUCCESSFUL_CONNECT_RESPONSE = 2


class Package:
    def __init__(self, data: bytes):
        self.__data = data

    def get_data(self):
        return self.__data

    @staticmethod
    def from_json(json_value: str) -> 'Package':
        data = json_value.encode(StreamConfiguration.ENCODING_FORMAT)

        return Package(data)

    def to_json(self) -> str:
        return self.__data.decode(StreamConfiguration.ENCODING_FORMAT)

    def __repr__(self):
        return f'Package(data={self.__data})'