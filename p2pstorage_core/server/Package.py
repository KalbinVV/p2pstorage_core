import logging
import socket
from enum import IntEnum
import pickle
from typing import Any

from p2pstorage_core.server import StreamConfiguration
from p2pstorage_core.server.Exceptions import EmptyHeaderException


class PackageType(IntEnum):
    HOST_CONNECT_REQUEST = 1
    HOST_CONNECT_RESPONSE = 2
    CONNECTION_LOST = 3
    NEW_FILE = 4


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

    def send(self, host_socket: socket.socket):
        from p2pstorage_core.server.Header import Header

        logging.debug(f'Sending package {self}...')

        data_to_send = self.encode()

        size_of_data = len(data_to_send)

        header = Header(size_of_data)

        header.send(host_socket)
        host_socket.send(data_to_send)

    def __repr__(self) -> str:
        return f'Package(data={self.__data}, type={self.__type})'

    @staticmethod
    def recv(host_socket: socket.socket):
        from p2pstorage_core.server.Header import Header

        header_data = host_socket.recv(StreamConfiguration.HEADER_SIZE)

        logging.debug(f'Receiving header data {header_data}...')

        if not header_data:
            raise EmptyHeaderException

        header = Header.decode(header_data)

        logging.debug(f'Receive header {header}!')

        package = header.load_package(host_socket)

        logging.debug(f'Receive package {package}!')

        return package

    @staticmethod
    def decode(obj: bytes):
        package: 'Package' = pickle.loads(obj)

        return package


class ConnectionRequestPackage(Package):
    def __init__(self):
        super().__init__(None, PackageType.HOST_CONNECT_REQUEST)


class ConnectionResponsePackage(Package):
    def __init__(self, connection_approved: bool = True, reject_reason: str = ''):
        super().__init__((connection_approved, reject_reason), PackageType.HOST_CONNECT_RESPONSE)

    def is_connection_approved(self) -> bool:
        return self.get_data()[0]

    def get_reason(self) -> bool:
        return self.get_data()[1]


class ConnectionLostPackage(Package):
    def __init__(self, reason: str = '!'):
        super().__init__(reason, PackageType.CONNECTION_LOST)


class NewFilePackage(Package):
    def __init__(self, file_name: str, file_size: int):
        super().__init__({
            'file_name': file_name,
            'file_size': file_size
        }, PackageType.NEW_FILE)

    def get_file_name(self) -> str:
        return self.get_data()['file_name']

    def get_file_size(self) -> int:
        return self.get_data()['file_size']
