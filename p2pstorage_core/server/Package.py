import socket
from enum import IntEnum
import pickle
from typing import Any

from p2pstorage_core.helper_classes.SocketAddress import SocketAddress


class PackageType(IntEnum):
    HOST_CONNECT_REQUEST = 1
    HOST_SUCCESSFUL_CONNECT_RESPONSE = 2


class Package:
    def __init__(self, data: Any, type_of_package: PackageType):
        self.__data = data
        self.__type = type_of_package

    def get_data(self) -> Any:
        return self.__data

    def get_type(self) -> PackageType:
        return self.__type

    def encode(self) -> bytes:
        return pickle.dumps(self)

    def send(self, host_socket: socket.socket, host_address: SocketAddress) -> None:
        from p2pstorage_core.server.Header import Header

        data_to_send = self.encode()

        size_of_data = len(data_to_send)

        header = Header(size_of_data, host_address)

        header.send(host_socket)
        host_socket.send(data_to_send)

    def __repr__(self) -> str:
        return f'Package(data={self.__data}, type={self.__type})'

    @staticmethod
    def decode(obj: bytes) -> 'Package':
        package: 'Package' = pickle.loads(obj)

        return package
